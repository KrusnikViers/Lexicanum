from typing import List, Dict, Generator

import mwparserfromhell as mwph

from core.util import if_none


class MarkupTree:
    def __init__(self, name: str, level: int, parent):
        self.name = name
        self.level = level
        self.plain_args: List[str] = []
        self.keyed_args: Dict[str, str] = {}

        self.children: List[MarkupTree] = []
        self.parent: MarkupTree | None = parent

    @classmethod
    def build(cls, raw_wiki_title: str, raw_wiki_text: str) -> 'MarkupTree':
        root = cls(raw_wiki_title.strip(), level=-1, parent=None)
        root._expand(mwph.parse(raw_wiki_text, skip_style_tags=True))
        return root

    def children_recursive(self) -> Generator['MarkupTree', None, None]:
        for child_node in self.children:
            yield child_node
            yield from child_node.children_recursive()

    def _expand(self, mwph_node: mwph.wikicode.Wikicode):
        # Meeting header switches parent for all the following nodes in sequential order, so we're keeping current
        # parent node as a separate variable.
        current_parent = self
        for mwph_child_node in mwph_node.nodes:
            if isinstance(mwph_child_node, mwph.nodes.Heading):
                current_parent = if_none(current_parent._expand_from_heading(mwph_child_node), current_parent)
            elif isinstance(mwph_child_node, mwph.nodes.Template):
                current_parent._expand_from_template(mwph_child_node)

    def _expand_from_heading(self, mwph_heading: mwph.nodes.Heading) -> 'MarkupTree':
        # Going up the parsing tree until we found header of lower level than the current one.
        current_parent = self
        while current_parent.level >= mwph_heading.level:
            current_parent = current_parent.parent

        heading_node = MarkupTree(str(mwph_heading.title).strip(), mwph_heading.level, parent=current_parent)
        heading_node._expand(mwph_heading.title)

        current_parent.children.append(heading_node)
        return heading_node

    def _expand_from_template(self, mwph_template: mwph.nodes.Template):
        template_node = MarkupTree(str(mwph_template.name).strip(), self.level + 1, parent=self)

        for param in mwph_template.params:
            if param.showkey:
                template_node.keyed_args[str(param.name).strip()] = str(param.value).strip()
                template_node._expand(param.name)
                template_node._expand(param.value)
            else:
                template_node.plain_args.append(str(param.value).strip())
                template_node._expand(param.value)
        self.children.append(template_node)

    def __str__(self) -> str:
        indent = 2 * (self.level + 1)
        result = ' ' * indent + '{}: {}'.format(self.level, self.name[:30])
        for arg in self.plain_args:
            result += '\n' + ' ' * indent + ' -{}'.format(arg[:30])
        for arg_key, arg_value in self.keyed_args.items():
            result += '\n' + ' ' * indent + ' -{} = {}'.format(arg_key[:30], arg_value[:30])
        for child in self.children:
            result += '\n' + str(child)
        return result
