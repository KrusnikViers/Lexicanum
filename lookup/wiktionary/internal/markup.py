from typing import List, Dict

import mwparserfromhell as mwph


class WikitextDataNode:
    def __init__(self, name: str):
        self.name = name
        self.plain_args: List[str] = []
        self.keyed_args: Dict[str, str] = {}

    def __str__(self, indent=0):
        return ' ' * indent + '{}: {} | {}'.format(self.name,
                                                   '|'.join(self.plain_args),
                                                   '|'.join(['{}={}'.format(x, y) for x, y in self.keyed_args.items()]))


class WikitextTreeNode:
    def __init__(self, title: str, level: int):
        self.title = title
        self.level = level
        self.nodes: List[WikitextDataNode] = []
        self.children: List[WikitextTreeNode] = []

    def __str__(self):
        indent = (self.level + 1) * 2
        result = ' ' * indent + '-{} [{}]'.format(self.title, self.level)
        for node in self.nodes:
            result += '\n' + node.__str__(indent + 1)
        for child in self.children:
            result += '\n' + str(child)
        return result


# Returns root section with empty title and -1 level.
def build_tree_from_markup(raw_wikitext: str, wiki_title: str) -> WikitextTreeNode:
    article = mwph.parse(raw_wikitext)
    structure_stack = [WikitextTreeNode(title=wiki_title, level=-1)]
    for parsed_node in article.nodes:
        if isinstance(parsed_node, mwph.nodes.Heading):
            while structure_stack[-1].level >= parsed_node.level:
                structure_stack.pop()
            new_section = WikitextTreeNode(title=parsed_node.title, level=parsed_node.level)
            structure_stack[-1].children.append(new_section)
            structure_stack.append(new_section)
            continue
        if isinstance(parsed_node, mwph.nodes.Template):
            new_node = WikitextDataNode(parsed_node.name)
            for param in parsed_node.params:
                if param.showkey:
                    new_node.keyed_args[str(param.name)] = str(param.value)
                else:
                    new_node.plain_args.append(str(param.value))
            structure_stack[-1].nodes.append(new_node)

    return structure_stack[0]
