import unittest
import subprocess
import sys

from tools.project_spec import BATTERY_BAY, BOX, ELECTRICAL, LABEL, PANEL_FEATURES


class ProjectSpecTest(unittest.TestCase):
    def test_envelope_fits_print_bed(self):
        self.assertEqual(
            (BOX["width"], BOX["height"], BOX["depth"]),
            (200, 160, 52),
        )
        self.assertLessEqual(max(BOX["width"], BOX["height"]), 220)

    def test_led_currents_are_below_twenty_milliamps(self):
        self.assertEqual(ELECTRICAL["resistor"], 330)
        for forward_voltage in ELECTRICAL["led_forward_voltages"].values():
            current = (
                ELECTRICAL["supply_max"] - forward_voltage
            ) / ELECTRICAL["resistor"]
            self.assertLess(current, 0.0201)

    def test_features_have_safe_margin(self):
        for feature in PANEL_FEATURES:
            self.assertGreaterEqual(feature["x"] - feature["radius"], 8)
            self.assertGreaterEqual(feature["y"] - feature["radius"], 8)
            self.assertLessEqual(
                feature["x"] + feature["radius"], BOX["width"] - 8
            )
            self.assertLessEqual(
                feature["y"] + feature["radius"], BOX["height"] - 8
            )

    def test_label_bleed(self):
        self.assertEqual(
            (LABEL["width"], LABEL["height"], LABEL["bleed"]),
            (204, 164, 2),
        )

    def test_battery_bay_holds_two_half_closed_2xaa_packs(self):
        self.assertEqual(BATTERY_BAY.get("holder_count"), 2)
        self.assertEqual(
            (BATTERY_BAY["width"], BATTERY_BAY["height"], BATTERY_BAY["depth"]),
            (62, 68, 18),
        )
        self.assertEqual((BATTERY_BAY["x"], BATTERY_BAY["y"]), (69, 46))

    def test_panel_cutouts_match_the_purchased_components(self):
        features = {feature["id"]: feature for feature in PANEL_FEATURES}
        expected_diameters = {
            "red_led": 10.2,
            "yellow_led": 10.2,
            "green_led": 10.2,
            "switch_led": 10.2,
            "dimmer_led": 10.2,
            "red_button": 12.2,
            "yellow_button": 12.2,
            "green_button": 16.2,
            "rocker": 20.2,
            "buzzer_button": 16.2,
        }
        for feature_id, expected_diameter in expected_diameters.items():
            self.assertEqual(features[feature_id]["kind"], "circle")
            self.assertAlmostEqual(features[feature_id]["radius"] * 2, expected_diameter)

    def test_dimensions_generator_runs_as_a_script(self):
        result = subprocess.run(
            [sys.executable, "tools/generate_dimensions.py"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
