import glob
from pathlib import Path
from subprocess import run

import PySide2

_GEN_FILE_SUFFIX = '_uic.py'

# This script relies on a multiple assumptions regarding your project:
# - This script is placed one level below project root (e.g. in "build_tools" directory).
# - You have top-level "ui" directory with nested "gen" directory.
# - Content of "ui/gen" directory is ok to be overwritten.
# - All files that you want to convert (and none other) have .ui extension and placed within "ui" directory.
#
# File /ui/<some_path>/<file_name>.ui will be translated into /ui/gen/<some_path>/<file_name>_uic.py.

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

# Converting UI files.
for input_file_strpath in glob.glob(ui_files_dir_strpath + '**/*.ui', recursive=True):
    input_file = Path(input_file_strpath)
    output_file_strpath = ui_files_dir_strpath + '/gen/' + input_file.stem + _GEN_FILE_SUFFIX
    print('Converting {} => {}...'.format(input_file_strpath, output_file_strpath))
    uic_process = run([qt_uic_path, '-g', 'python', '-o', output_file_strpath, input_file_strpath],
                      timeout=30.0, check=True)

print('---\nAll done!')
