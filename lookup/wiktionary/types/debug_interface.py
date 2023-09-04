# This class can be provided to the lookup methods. If it is present, methods are expected to pass detailed info to it.
# Display is handled separately.
from typing import List

from lookup.wiktionary.types.definition_components import DefinitionComponent
from lookup.wiktionary.types.markup_tree import MarkupTree


class DebugInterface:
    def progress_message(self, message: str):
        raise NotImplementedError

    def progress_rich_message(self, title: str, message: str):
        raise NotImplementedError

    def show_raw_wiki_content(self, wiki_title: str, language: str, content: str):
        raise NotImplementedError

    def show_markup_tree(self, wiki_title: str, language: str, tree: MarkupTree):
        raise NotImplementedError

    def show_components_list(self, wiki_title: str, language: str, components: List[DefinitionComponent]):
        raise NotImplementedError
