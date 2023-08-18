import glob
from pathlib import Path
from subprocess import run

_GEN_FILE_SUFFIX = '_uic.py'

# This script relies on a multiple assumptions regarding your project:
# - This script is placed one level below project root (e.g. in "build_tools" directory).
# - You have top-level "ui" directory with nested "gen" directory.
# - Content of "ui/gen" directory is ok to be overwritten.
# - All files that you want to convert (and none other) have .ui extension and placed within "ui" directory.
#
# File /ui/<some_path>/<file_name>.ui will be translated into /ui/gen/<some_path>/<file_name>_uic.py.

# Looking for UI files directory.
ui_files_dir = (Path(__file__).parent.parent / 'ui').resolve()
gen_files_dir = ui_files_dir / 'gen'
assert ui_files_dir.is_dir()
print('Target UI directory: {}'.format(str(ui_files_dir)))
print()

# Removing previously generated files.
print('Cleaning {}'.format(str(gen_files_dir) + '...'))
generated_files_pattern = gen_files_dir / '**' / '*{}'.format(_GEN_FILE_SUFFIX)
for existing_file_strpath in glob.glob(str(generated_files_pattern), recursive=True):
    existing_file = Path(existing_file_strpath)
    assert existing_file.is_file()
    existing_file.unlink()

# Converting UI files.
files_to_convert_pattern = ui_files_dir / '**' / '*.ui'
for input_file_strpath in glob.glob(str(files_to_convert_pattern), recursive=True):
    input_file = Path(input_file_strpath)
    new_file_name = input_file.name[:-3] + _GEN_FILE_SUFFIX
    output_file = gen_files_dir / input_file.relative_to(ui_files_dir).with_name(new_file_name)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    print('Converting {} => {}...'.format(str(input_file), str(output_file)))
    uic_process = run(['pyside6-uic', '-g', 'python', '-o', str(output_file), str(input_file)],
                      timeout=30.0, check=True)

print('---\nAll done!')
