# STL export

[English](README.md) | [Türkçe](README.tr.md)

Generated STL files are intentionally not committed. Install OpenSCAD, then
run the following commands from the repository root:

```sh
make stl
make validate
```

The export creates:

- `activity-box-body.stl`
- `activity-box-back.stl`
- `activity-box-dial.stl`
- `snap-fit-test.stl`
- `component-fit-test.stl`

Print and verify the two test models before printing the enclosure.

## Print orientation

- Body: print with the front face down on the build plate.
- Back plate: print with the outer face down on the build plate.
- Dial: print with the flange down on the build plate.
