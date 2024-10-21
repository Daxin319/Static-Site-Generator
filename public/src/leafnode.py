from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value == None:
            raise ValueError
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return str(self.value)
        props_string = self.props_to_html() if self.props else ""
        if self.tag == "img":
            return f"<{self.tag}{props_string} />"
        else:
            return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"
