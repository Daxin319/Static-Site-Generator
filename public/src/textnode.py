from enum import Enum
from leafnode import *

class TextType(Enum):
    HTML = "html"
    BOLD = "bold"
    TEXT = "text"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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