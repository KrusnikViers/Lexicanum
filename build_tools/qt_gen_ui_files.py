# Add this script as a build step in your process, and make sure to run it every time UI files were changed.
# This file relies on being located in <project root>/build_tools package.
#
# Script will generate python versions for all UI files in your project by the following rule:
# <path>/<filename><_UI_FILE_SUFFIX> => <path>/<filename><_GEN_FILE_SUFFIX>.
# Do not edit generated files manually, as all changes will be overwritten on the next run. Old generated files will be
# removed on each run, based on _GEN_FILE_SUFFIX.


import glob
from pathlib import Path
from subprocess import run

_GEN_FILE_SUFFIX = '_uic.py'
_UI_FILE_SUFFIX = '.ui'


def _assert_is_file(file: Path):
    if not file.is_file():
        raise ValueError(f"{str(file.resolve())} cannot be treated as a file")


def remove_generated_files(target_dir: Path) -> int:
    existing_gen_files_pattern = target_dir / '**' / '*{}'.format(_GEN_FILE_SUFFIX)
    existing_gen_files_list = glob.glob(str(existing_gen_files_pattern), recursive=True)
    existing_gen_files_count = len(existing_gen_files_list)
    print('{} generated files found.'.format(existing_gen_files_count))
    if existing_gen_files_count == 0:
        return existing_gen_files_count

    print('Removing...')
    for existing_gen_file_path in existing_gen_files_list:
        existing_gen_file = Path(existing_gen_file_path)
        _assert_is_file(existing_gen_file)
        existing_gen_file.unlink()
    print('Done.\n')
    return len(existing_gen_files_list)


def generate_files(target_dir: Path) -> int:
    ui_files_pattern = target_dir / '**' / '*{}'.format(_UI_FILE_SUFFIX)
    ui_files_list = glob.glob(str(ui_files_pattern), recursive=True)
    ui_files_count = len(ui_files_list)
    print('{} UI files found.'.format(ui_files_count))
    if ui_files_count == 0:
        return ui_files_count

    print('Generating...')
    for ui_file_path in ui_files_list:
        ui_file = Path(ui_file_path)
        _assert_is_file(ui_file)
        gen_file_name = ui_file.name[:-len(_UI_FILE_SUFFIX)] + _GEN_FILE_SUFFIX
        gen_file = ui_file.with_name(gen_file_name)
        print('{} => {}'.format(str(ui_file.relative_to(target_dir)), gen_file.name))
        run(['pyside6-uic', '-g', 'python', '-o', str(gen_file), str(ui_file)], timeout=30.0, check=True)
    print('Done.\n')
    return len(ui_files_list)


def regenerate_files(target_dir: Path) -> None:
    print('Target directory: {}'.format(str(target_dir)))
    remove_generated_files(target_dir)
    generate_files(target_dir)
    print('All done!')


if __name__ == "__main__":  # pragma: no cover
    root_dir = Path(__file__).parent.parent.resolve()
    regenerate_files(root_dir)
