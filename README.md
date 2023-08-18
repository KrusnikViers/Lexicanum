# Lexicanum

A GUI utility to build and edit Anki decks for foreign words

## Development flow

General conventions regarding the release process and versioning is described in the [VERSIONS](VERSIONS.md) file.

The features list is split between github issues and the [FEATURES](FEATURES.md) file. Expectation is that eventually
the [FEATURES](FEATURES.md) file will be completely removed.

## Working with project

In the text below, `ROOT_DIR` should be replaced with the path to the directory containing this README file. A working
directory should be set to the `ROOT_DIR` as well, unless specified otherwise.

### Generate UI files

The project uses Qt framework, so to build it from sources you will need to generate python files for UI files before
referring to them from code. To do so, run `ROOT_DIR/build_tools/convert_ui_files.py`. Important: this code will use a
generator tool from PySide package available, and will look for the Qt-specific files in the `../../ui` directory
recursively, regardless of the working directory.

### Run project without .exe

Run `ROOT_DIR/main.py`. You will need to generate UI files first.

### Building .exe

To build an .exe file that would work under Windows OS, run `ROOT_DIR/build_tools/create_binary_win.bat`. It creates a
standalone portable executable file, that could be run without installing Python or dependency packages on the target
machine.

### Running unittests

Unittests are automatically discoverable, run `python -m unittest discover -s ROOT_DIR`

### Refreshing test Wiktionary data

Some tests rely on cashed copy of data from Wiktionary. To refresh them,
run `ROOT_DIR/build_tools/refresh_wiktionary_test_data.py`. If you are creating new localized data parser, please make a
copy of `base` tests directory: cached pages are exact wiktionary content, and thus overall project license does not
apply to them.
