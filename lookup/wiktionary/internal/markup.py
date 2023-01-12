from typing import List, Dict

import mwparserfromhell as mwph


class WikitextContentNode:
    def __init__(self, name: str, level: int, parent=None):
        self.name = name
        self.level = level
        self.plain_args: List[str] = []
        self.keyed_args: Dict[str, str] = {}

        self.children: List[WikitextContentNode] = []
        self.parent: WikitextContentNode | None = parent

    def __str__(self) -> str:
        indent = 2 * (self.level + 1)
        result = ' ' * indent + '#{} :: {}'.format(self.level, self.name[:25])
        for arg in self.plain_args:
            result += '\n' + ' ' * indent + '- {}'.format(arg[:20])
        for arg_key, arg_value in self.keyed_args.items():
            result += '\n' + ' ' * indent + '- {}={}'.format(arg_key[:20], arg_key[:20])
        for child in self.children:
            result += '\n' + str(child)
        return result


def _expand_content_tree_from_wikicode(wikicode: mwph.wikicode.Wikicode, root: WikitextContentNode):
    current_root = root
    for parsed_node in wikicode.nodes:
        if isinstance(parsed_node, mwph.nodes.Heading):
            while current_root.level >= parsed_node.level:
                current_root = current_root.parent
            new_node = WikitextContentNode(str(parsed_node.title).strip(), parsed_node.level, parent=current_root)
            current_root.children.append(new_node)
            current_root = new_node
            _expand_content_tree_from_wikicode(parsed_node.title, current_root)
            continue
        if isinstance(parsed_node, mwph.nodes.Template):
            new_node = WikitextContentNode(str(parsed_node.name).strip(), current_root.level + 1, parent=current_root)
            current_root.children.append(new_node)
            for param in parsed_node.params:
                if param.showkey:
                    new_node.keyed_args[str(param.name).strip()] = str(param.value).strip()
                    _expand_content_tree_from_wikicode(param.name, new_node)
                    _expand_content_tree_from_wikicode(param.value, new_node)
                else:
                    new_node.plain_args.append(str(param.value).strip())
                    _expand_content_tree_from_wikicode(param.value, new_node)


def build_wiki_content_tree(raw_wiki_text: str, wiki_page_title: str) -> WikitextContentNode:
    parsed_tree = mwph.parse(raw_wiki_text)
    root = WikitextContentNode(wiki_page_title, -1)
    _expand_content_tree_from_wikicode(parsed_tree, root)
    return root
