import pathlib
import re
import subprocess
import unittest


class CadSourceTest(unittest.TestCase):
    @staticmethod
    def _number(text, name):
        match = re.search(rf"^{name} = ([0-9.]+);$", text, re.MULTILINE)
        if not match:
            raise AssertionError(f"Missing numeric OpenSCAD assignment: {name}")
        return float(match.group(1))

    @staticmethod
    def _point(text, name):
        match = re.search(
            rf"^{name} = \[([0-9.]+), ([0-9.]+)\];$", text, re.MULTILINE
        )
        if not match:
            raise AssertionError(f"Missing OpenSCAD point assignment: {name}")
        return tuple(float(value) for value in match.groups())

    def test_required_modules_and_generated_include(self):
        text = pathlib.Path("cad/activity_box.scad").read_text(encoding="utf-8")
        self.assertIn("include <generated_dimensions.scad>", text)
        for name in ("body", "back", "dial", "snap_fit_test", "component_fit_test"):
            self.assertIn(f"module {name}(", text)

    def test_stl_target_exports_component_fit_coupon(self):
        result = subprocess.run(
            ["make", "-n", "stl"],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("output/stl/component-fit-test.stl", result.stdout)
        self.assertIn('part="component_test"', result.stdout)

    def test_dial_flange_clears_led_guard_and_remains_captive(self):
        cad = pathlib.Path("cad/activity_box.scad").read_text(encoding="utf-8")
        dimensions = pathlib.Path("cad/generated_dimensions.scad").read_text(
            encoding="utf-8"
        )
        flange_diameter = self._number(cad, "dial_flange_d")
        flange_thickness = self._number(cad, "dial_flange_t")
        opening_diameter = self._number(dimensions, "dial_opening_d")
        led = self._point(dimensions, "pos_dimmer_led")
        dial = self._point(dimensions, "pos_dial")

        center_distance = ((led[0] - dial[0]) ** 2 + (led[1] - dial[1]) ** 2) ** 0.5
        led_guard_diameter = 16.0  # Existing, already-printed body geometry.
        clearance = center_distance - (flange_diameter + led_guard_diameter) / 2
        capture_overlap = (flange_diameter - opening_diameter) / 2

        self.assertGreaterEqual(clearance, 1.0)
        self.assertGreaterEqual(capture_overlap, 1.0)
        self.assertGreaterEqual(flange_thickness, 4.0)

    def test_cad_protects_and_mounts_the_purchased_parts(self):
        text = pathlib.Path("cad/activity_box.scad").read_text(encoding="utf-8")
        for module in (
            "open_led_guard",
            "pot_mount_bridge",
            "battery_center_divider",
        ):
            self.assertIn(f"module {module}(", text)
        self.assertIn("buzzer_port_depth", text)

    def test_component_coupon_contains_all_fit_choices(self):
        text = pathlib.Path("cad/generated_dimensions.scad").read_text(
            encoding="utf-8"
        )
        for assignment in (
            "fit_size = [200, 76]",
            "fit_led_diameters = [10.0, 10.2]",
            "fit_dc184_diameters = [12.0, 12.2]",
            "fit_dc180_diameters = [16.0, 16.2]",
            "fit_dc131a_diameters = [20.0, 20.2]",
            "fit_pot_bushing_diameters = [7.0, 7.2]",
            "fit_shaft_diameters = [5.8, 6.0, 6.2]",
            "fit_dc120_sizes = [[19.0, 13.0], [19.4, 13.4]]",
        ):
            self.assertIn(assignment, text)


if __name__ == "__main__":
    unittest.main()
