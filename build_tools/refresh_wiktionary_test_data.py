import glob
from pathlib import Path

from lookup.wiktionary.internal_logic.web_api import retrieve_articles


# Tries to fetch fresh wiktionary contents for linked pages. Returns True if content was updated.
def refresh_wiktionary_test_data(dry_run: bool) -> bool:
    localized_parsers_dir = (Path(__file__).parent.parent / 'lookup' / 'wiktionary' / 'languages').resolve()
    target_files_pattern = localized_parsers_dir / '**' / '*.txt'
    target_files = glob.glob(str(target_files_pattern), recursive=True)
    print('Updating {} files...'.format(len(target_files)))
    files_without_updates = 0
    for existing_file_strpath in target_files:
        existing_file = Path(existing_file_strpath)
        assert existing_file.is_file()

        with open(existing_file, 'r', encoding='utf-8') as file_to_read:
            title = file_to_read.readline().strip()
            language_code = file_to_read.readline().strip()
            file_to_read.readline().strip()  # Skip link to the original page
            old_content = file_to_read.read()

        new_content_status = retrieve_articles([title], language_code)
        if new_content_status.is_error():
            print('Error: {}, skipping {}:{} from {}...'.format(
                new_content_status.status, title, language_code, existing_file_strpath))
            continue
        if len(new_content_status.value) != 1:
            print('Error: retrieved {} articles, skipping {}:{} from {}...'.format(
                len(new_content_status.value), title, language_code, existing_file_strpath))
            continue

        new_content = new_content_status.value[0]
        if new_content.content.strip() != old_content.strip():
            if not dry_run:
                with open(existing_file, 'w', encoding='utf-8') as file_to_write:
                    print(title, file=file_to_write)
                    print(language_code, file=file_to_write)
                    print('Original article URL: https://{}.wiktionary.org/wiki/{}'.format(language_code, title),
                          file=file_to_write)
                    print(new_content.content, file=file_to_write)
            print('{}:{} ({}) refreshed'.format(title, language_code, existing_file_strpath))
        else:
            files_without_updates += 1
    print('All done! Files without updates: {}'.format(files_without_updates))
    return files_without_updates != len(target_files)


if __name__ == '__main__':
    refresh_wiktionary_test_data(dry_run=False)
