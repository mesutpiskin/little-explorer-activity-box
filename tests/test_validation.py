import pathlib
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


if __name__ == "__main__":
    unittest.main()
