from enum import Enum
from leafnode import * # leafnodes are also a child class of htmlnode

# Enum to hold valid text types
class TextType(Enum):
    HTML = "html"
    BOLD = "bold"
    TEXT = "text"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

#TextNode class, child of HTMLNode
class TextNode:
    def __init__(self, text, text_type=TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        if self.text == obj.text and self.text_type == obj.text_type and self.url == obj.url:
            return True
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

#function to convert textnodes to html formatted leafnodes
def textnode_to_htmlnode(textnode):
    match textnode.text_type:
        case TextType.TEXT:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode('b', textnode.text)
        case TextType.ITALIC:
            return LeafNode('i', textnode.text)
        case TextType.CODE:
            return LeafNode('code', textnode.text)
        case TextType.LINK:
            return LeafNode('a', textnode.text, {'href': f'{textnode.url}'})
        case TextType.IMAGE:
            return LeafNode('img', "", {'src': textnode.url, 'alt': textnode.text})
        case _:
            raise ValueError(f"Unexpected text type: {textnode.text_type}")

# function to convert raw markdown to list of TextNodes        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT :
            new_nodes.append(node)
        else:
            first_pos = node.text.find(delimiter) #find first delimiter
            second_pos = node.text.find(delimiter, first_pos + 1)
            if second_pos == -1 and first_pos != -1:
                raise Exception('<----------------------Invalid markdown syntax, no closing delimiter found or empty set of delimiters found---------------------->')
            if first_pos == -1:
                new_nodes.append(TextNode(node.text))
            else:
                if node.text[:first_pos]:
                    new_nodes.append(TextNode(node.text[:first_pos]))
                new_nodes.append(TextNode(node.text[first_pos + len(delimiter):second_pos], text_type))
                if node.text[second_pos + len(delimiter):]:
                    new_nodes.extend(split_nodes_delimiter([TextNode(node.text[second_pos + len(delimiter):])], delimiter, text_type))
    return new_nodes
                
            

debug_node = TextNode("This line has a `code block` section.")
split_nodes_delimiter([debug_node], '`', TextType.CODE)