from typing import Generator, Dict, List

from lookup.wiktionary.internal.markup_tree import MarkupTreeNode


# Iterates over all nodes children depth-first
def all_children_recursive(tree_node: MarkupTreeNode) -> Generator[MarkupTreeNode, None, None]:
    for child_node in tree_node.children:
        yield child_node
        yield from all_children_recursive(child_node)


# Generator zips translations as series of lists with following logic:
# - Lists contain first, second, third... etc. translation options for each language
# - Languages in each list is ordered the same as their language codes
def merge_translation_dict(translations: Dict[str, List[str]],
                           language_codes: List[str]) -> Generator[List[str], None, None]:
    translations_lists = [translations[code] for code in language_codes if code in translations and translations[code]]
    if not translations_lists:
        return
    outputted = set()
    max_len = max(map(len, translations_lists))
    for i in range(0, max_len):
        output = [translations_list[i] for translations_list in translations_lists
                  if i < len(translations_list) and translations_list[i] not in outputted]
        for word in output:
            outputted.add(word)
        yield output
