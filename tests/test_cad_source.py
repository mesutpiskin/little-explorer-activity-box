import pathlib
import unittest


class CadSourceTest(unittest.TestCase):
    def test_required_modules_and_generated_include(self):
        text = pathlib.Path("cad/activity_box.scad").read_text(encoding="utf-8")
        self.assertIn("include <generated_dimensions.scad>", text)
        for name in ("body", "back", "dial", "snap_fit_test"):
            self.assertIn(f"module {name}(", text)

    def test_captive_dial_dimensions_are_physically_consistent(self):
        text = pathlib.Path("cad/activity_box.scad").read_text(encoding="utf-8")
        self.assertIn("dial_grip_d = 32", text)
        self.assertIn("dial_flange_d = 46", text)


if __name__ == "__main__":
    unittest.main()
