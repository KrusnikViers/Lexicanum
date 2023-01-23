from typing import List, Dict

import mwparserfromhell as mwph


class MarkupTreeNode:
    def __init__(self, name: str, level: int, parent=None):
        self.name = name
        self.level = level
        self.plain_args: List[str] = []
        self.keyed_args: Dict[str, str] = {}

        self.children: List[MarkupTreeNode] = []
        self.parent: MarkupTreeNode | None = parent

    def __str__(self) -> str:
        indent = 2 * (self.level + 1)
        result = ' ' * indent + '#{} :: {}'.format(self.level, self.name[:25])
        for arg in self.plain_args:
            result += '\n' + ' ' * indent + '- {}'.format(arg[:20])
        for arg_key, arg_value in self.keyed_args.items():
            result += '\n' + ' ' * indent + '- {}={}'.format(arg_key[:20], arg_value[:20])
        for child in self.children:
            result += '\n' + str(child)
        return result


# Returns new parent in the order of parsing, as all templates going after should belong to created section.
def _expand_from_heading(mwph_heading: mwph.nodes.Heading, parent: MarkupTreeNode) -> MarkupTreeNode:
    current_root = parent
    while current_root.level >= mwph_heading.level:
        current_root = current_root.parent
    new_node = MarkupTreeNode(str(mwph_heading.title).strip(), mwph_heading.level, parent=current_root)
    current_root.children.append(new_node)
    _expand_content_tree_from_wikicode(mwph_heading.title, new_node)
    return new_node


def _expand_from_template(mwph_template: mwph.nodes.Template, parent: MarkupTreeNode):
    new_node = MarkupTreeNode(str(mwph_template.name).strip(), parent.level + 1, parent=parent)
    parent.children.append(new_node)
    for param in mwph_template.params:
        if param.showkey:
            new_node.keyed_args[str(param.name).strip()] = str(param.value).strip()
            _expand_content_tree_from_wikicode(param.name, new_node)
            _expand_content_tree_from_wikicode(param.value, new_node)
        else:
            new_node.plain_args.append(str(param.value).strip())
            _expand_content_tree_from_wikicode(param.value, new_node)


def _expand_content_tree_from_wikicode(mwph_parent: mwph.wikicode.Wikicode, parent: MarkupTreeNode) -> MarkupTreeNode:
    current_root = parent
    for mwph_node in mwph_parent.nodes:
        if isinstance(mwph_node, mwph.nodes.Heading):
            current_root = _expand_from_heading(mwph_node, current_root)
        elif isinstance(mwph_node, mwph.nodes.Template):
            _expand_from_template(mwph_node, current_root)
    return current_root


def build_wiki_content_tree(raw_wiki_text: str, raw_wiki_title: str) -> MarkupTreeNode:
    mwph_tree = mwph.parse(raw_wiki_text)
    root = MarkupTreeNode(raw_wiki_title.strip(), -1)
    _expand_content_tree_from_wikicode(mwph_tree, root)
    return root
