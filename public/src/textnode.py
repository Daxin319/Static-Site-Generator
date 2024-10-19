from enum import Enum

class NodeType(Enum):
    HTML = "html"
    LEAF = "leaf"
    TEXT = "text"

class TextNode(TEXT, TEXT_TYPE, URL):
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
