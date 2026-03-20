# Lexicanum

[![codecov](https://codecov.io/gh/KrusnikViers/Lexicanum/graph/badge.svg)](https://codecov.io/gh/KrusnikViers/Lexicanum)
[![Maintainability](https://qlty.sh/gh/KrusnikViers/projects/Lexicanum/maintainability.svg)](https://qlty.sh/gh/KrusnikViers/projects/Lexicanum)

Application to simplify creating language-learning Anki cards.  
Other files: [License file (MIT)](LICENSE), [Features tracker](FEATURES.md)

### Suggested Workflows / Run Configurations
* `Gen UI`
  * Python script `$ProjectFileDir$/build_tools/qt_gen_ui_files.py`
  * Add this step as a pre-requisite for all the next steps
* `Run App`
  * Python script `$ProjectFileDir$/main.py`
* `Run Tests`
  * Unittests in project root directory, pattern `*_test.py`
* `Build Binary`
  * Python Module `PyInstaller`
  * Arguments: `$ProjectFileDir$/build_tools/pyinstaller/binary.spec`

### Adding Qt Designer in PyCharm

Settings ⇒ Tools ⇒ External Tools  
Program: `$ProjectFileDir$\.venv\Lib\site-packages\PySide6\designer.exe`  
Arguments: `$FilePath$`  
Directory: `$ProjectFileDir$`

### Versions and release process

Project has two hardcoded version numbers. Updating major version resets minor one to zero.

1. `PROJECT_COMPATIBILITY_VERSION`  
   Increased when changes make new version incompatible with the previous one in any way.
2. `PROJECT_FEATURE_PACK_VERSION`  
   Increased with significant changes from the user point of view.

Separately, all builds from GitHub Actions will bake "branch:commit" as part of the version info, to simplify finding
the exact build. All local builds will have "local:unknown" stated there.
