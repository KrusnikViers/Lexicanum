# General project name and version constants. Refer to these constants whenever possible.
# These values can be used for defining compatibility or storing project-related data, and should not be changed
# without a good reason.
from base import git_info

PUBLISHER_NAME = "KrusnikViers"
PROJECT_NAME = "Lexicanum"
PROJECT_URL = "https://github.com/KrusnikViers/Lexicanum"

_PROJECT_COMPATIBILITY_VERSION: int = 0
_PROJECT_FEATURE_PACK_VERSION: int = 0

# Git branch name & commit hash, 'local' if not build on the server.
_PROJECT_BUILD_TYPE: str = git_info.PROJECT_BUILD_TYPE
_PROJECT_SHORT_HASH: str = git_info.PROJECT_HASH[:7]

VERSION = f'v{_PROJECT_COMPATIBILITY_VERSION}.{_PROJECT_FEATURE_PACK_VERSION}'
VERSION_FULL = f'{VERSION} ({_PROJECT_BUILD_TYPE}:{_PROJECT_SHORT_HASH})'
PROJECT_NAME_VERSION = f'{PROJECT_NAME} {VERSION}'
