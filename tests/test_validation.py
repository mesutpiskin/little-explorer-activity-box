import pathlib
import subprocess
import tempfile
import unittest

from tools.validate_outputs import (
    REQUIRED_OUTPUTS,
    is_closed_manifold,
    validate_project,
)


class ValidationTest(unittest.TestCase):
    def test_required_outputs_include_all_printable_parts(self):
        expected = {
            pathlib.Path("output/stl/activity-box-body.stl"),
            pathlib.Path("output/stl/activity-box-back.stl"),
            pathlib.Path("output/stl/activity-box-dial.stl"),
            pathlib.Path("output/stl/snap-fit-test.stl"),
            pathlib.Path("output/stl/component-fit-test.stl"),
        }
        self.assertTrue(expected <= set(REQUIRED_OUTPUTS))

    def test_required_outputs_include_both_language_sets(self):
        expected = {
            pathlib.Path("artwork/activity-box-label.svg"),
            pathlib.Path("artwork/tr/activity-box-label.svg"),
            pathlib.Path("docs/assembly.md"),
            pathlib.Path("docs/tr/assembly.md"),
            pathlib.Path("docs/component-placement-guide.png"),
            pathlib.Path("docs/tr/component-placement-guide.png"),
        }
        self.assertTrue(expected <= set(REQUIRED_OUTPUTS))

    def test_tetrahedron_is_closed_manifold(self):
        a, b, c, d = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
        triangles = [(a, c, b), (a, b, d), (b, c, d), (c, a, d)]
        self.assertTrue(is_closed_manifold(triangles))

    def test_single_triangle_is_not_closed_manifold(self):
        self.assertFalse(
            is_closed_manifold([((0, 0, 0), (1, 0, 0), (0, 1, 0))])
        )

    def test_current_project_validates_when_stl_export_is_deferred(self):
        errors, warnings = validate_project(
            pathlib.Path("."), allow_missing_stl=True
        )
        self.assertEqual(errors, [])
        self.assertTrue(any("STL" in warning for warning in warnings))

    def test_validator_detects_private_references_in_other_text_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            private_reference = "owner" + "@" + "example.com or use /" + "home/alice/private.scad"
            (root / "notes.md").write_text(
                f"Contact {private_reference}",
                encoding="utf-8",
            )
            errors, _ = validate_project(root, allow_missing_stl=True)
        self.assertTrue(any("private environment reference" in error for error in errors))

    def test_validator_scans_public_python_but_skips_ignored_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q", root], check=True)
            (root / ".gitignore").write_text("ignored.py\n", encoding="utf-8")
            private_path = "/" + "Users/alice/private.py"
            (root / "public.py").write_text(private_path, encoding="utf-8")
            (root / "ignored.py").write_text(private_path, encoding="utf-8")

            errors, _ = validate_project(root, allow_missing_stl=True)
            private_errors = [
                error for error in errors if "private environment reference" in error
            ]

            self.assertEqual(private_errors, ["private environment reference found in public.py"])


if __name__ == "__main__":
    unittest.main()
