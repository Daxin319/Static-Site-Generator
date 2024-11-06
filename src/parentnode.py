from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if not isinstance(children, list):
            raise ValueError("Parent Nodes must have children")
        super().__init__(tag, None, children, props)

    # function to convert properties to html format
    def to_html(self):
        if not self.tag:
            raise ValueError('no tag present')
        else:
            props_string = self.props_to_html() if self.props else ""
            child_string = "".join(node.to_html() for node in self.children)
            return f'<{self.tag}{props_string}>{child_string}</{self.tag}>'