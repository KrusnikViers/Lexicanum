from pathlib import Path
from typing import NamedTuple

_TEST_CONTENT_DIR_NAME = 'test_wiktionary_content'


class TestContent(NamedTuple):
    title: str
    language_code: str
    content: str


# First argument is local __file__ variable, to get correct relative path.
def get_test_content(file_var: str, file_name: str) -> TestContent:
    path: Path = Path(file_var).parent / _TEST_CONTENT_DIR_NAME / file_name
    assert path.is_file()
    with open(path, 'r', encoding='utf-8') as file_to_read:
        title = file_to_read.readline().strip()
        language_code = file_to_read.readline().strip()
        file_to_read.readline().strip()  # Skip link to the original page
        content = file_to_read.read()
    return TestContent(title=title, language_code=language_code, content=content)
