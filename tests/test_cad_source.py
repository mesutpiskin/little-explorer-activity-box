import pathlib
import subprocess
import unittest


class CadSourceTest(unittest.TestCase):
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

    def test_captive_dial_dimensions_are_physically_consistent(self):
        text = pathlib.Path("cad/activity_box.scad").read_text(encoding="utf-8")
        self.assertIn("dial_grip_d = 32", text)
        self.assertIn("dial_flange_d = 46", text)

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
