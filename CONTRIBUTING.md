# Contributing

[English](CONTRIBUTING.md) | [Türkçe](CONTRIBUTING.tr.md)

Contributions that improve safety, reproducibility, documentation, or printer
compatibility are welcome.

## Before changing dimensions

1. Print `component-fit-test.stl` and `snap-fit-test.stl`.
2. Record the printer, material, nozzle, layer height, and measured fit.
3. Change shared dimensions in `tools/project_spec.py` where possible.
4. Regenerate derived files instead of editing them by hand.

Do not change a hole or snap-fit dimension from an unverified catalog drawing
alone. Parts sold under the same name may have different batches and bezels.

## Development setup

```sh
python3 -m pip install -r requirements.txt
make dimensions artwork docs
make test
```

OpenSCAD is additionally required for:

```sh
make stl
make validate
```

`make validate-source` verifies all non-STL artifacts when OpenSCAD is not
available.

## Generated files

The English files in `artwork/` and `docs/` and their Turkish equivalents in
`artwork/tr/` and `docs/tr/` are generated. Edit the corresponding script in
`tools/`, regenerate both languages, and include the source and outputs in the
same change. Never move a cutout in one language only.

## Pull requests

- Keep changes focused and explain the physical reason for dimensional edits.
- Add or update a test before changing generator behavior.
- Run `make test` and `make validate-source` before submission.
- Include fit photos or measurements when changing physical tolerances.
- Do not include personal inventory, local paths, supplier accounts, or
  private reference photos.
- Never weaken the safety notice or remove the fuse from the documented power
  path without engineering evidence and review.

By contributing, you agree that your work is licensed according to
[`LICENSES/README.md`](LICENSES/README.md).
