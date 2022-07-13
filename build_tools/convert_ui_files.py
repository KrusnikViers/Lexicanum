import glob
from pathlib import Path
from subprocess import run

import PySide2

_GEN_FILE_SUFFIX = '_uic.py'

# This script makes multiple assertions regarding your project:
# - You have top-level "ui" directory
# - Generated files will be placed in "ui/gen" directory (should exist) with rest of the path untouched.

# Looking for the UIC tool. Make sure that requirements are installed!
qt_uic_path = str((Path(PySide2.__file__).parent / 'uic').resolve())
print('Qt converter to use: {}'.format(qt_uic_path))

# Looking for UI files directory.
ui_files_dir = (Path(__file__).parent.parent / 'ui').resolve()
assert ui_files_dir.is_dir()
ui_files_dir_strpath = str(ui_files_dir)
print('Target UI directory: {}'.format(ui_files_dir))
print()

# Removing previously generated files.
print('Cleaning {}'.format(ui_files_dir_strpath + '/gen/...'))
for existing_file_strpath in glob.glob(ui_files_dir_strpath + '/gen/**/*' + _GEN_FILE_SUFFIX, recursive=True):
    existing_file = Path(existing_file_strpath)
    assert existing_file.is_file()
    existing_file.unlink()

# Converting UI files one by one.
for input_file_strpath in glob.glob(ui_files_dir_strpath + '**/*.ui', recursive=True):
    input_file = Path(input_file_strpath)
    output_file_strpath = ui_files_dir_strpath + '/gen/' + input_file.stem + _GEN_FILE_SUFFIX
    print('Converting {} => {}...'.format(input_file_strpath, output_file_strpath))
    uic_process = run([qt_uic_path, '-g', 'python', '-o', output_file_strpath, input_file_strpath],
                      timeout=30.0, check=True)

print('---\nAll done!')
