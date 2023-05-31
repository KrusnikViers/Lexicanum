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
# - Previously met words are skipped
def merge_translation_dict(translations: Dict[str, List[str]],
                           language_codes: List[str]) -> List[str]:
    # List of translation options for each code, in |language_codes| order.
    translations_lists = [translations[code] for code in language_codes if code in translations and translations[code]]
    if not translations_lists:
        return []

    result = []
    already_in_result = set()
    max_language_code_list_len = max(map(len, translations_lists))
    for i in range(0, max_language_code_list_len):
        for translations_list in translations_lists:
            word = translations_list[i]
            if word in already_in_result:
                continue
            result.append(word)
    return result
