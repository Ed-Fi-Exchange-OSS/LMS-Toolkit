# Build Script

The `eng` directory contains a Python script, `build.py`, that supports
common development tasks on all of the packages in this repository. Usage:

```bash
python eng/build.py [command] [package]
```

Where `[command]` is one of:

| Command | Explanation |
| -- | -- |
| `install` | Install all dependencies |
| `test` | Run unit tests |
| `coverage` | Run unit tests with code coverage |
| `coverage:html` | Run unit tests with code coverage, exported to HTML |
| `coverage:xml` | Run unit tests with code coverage, exported to XML |
| `lint` | Run lint / style checks |
| `typecheck` | Run type checking |
| `typecheck:xml` | Run type checking, exported to XML |
| `build` | Build distribution packages |
| `publish` | Build and publish packages |

and where `[package]` is the name and path of a package, relative to the `src`
directory.

## Examples

### Run the linter on the Canvas Extractor

```bash
python eng/build.py lint canvas-extractor
```

### Run typecheck on the File Tester utility

```bash
python eng/build.py lint ../utils/file-tester
```

### Publish the Google Classroom Extractor to PyPi

```bash
TWINE_USERNAME="<pypi username>"
TWINE_PASSWORD="<pypi password>"

python eng/build.py publish google-classroom-extractor
```
