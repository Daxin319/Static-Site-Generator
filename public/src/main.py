from textnode import *
from parentnode import *
from leafnode import *
from htmlnode import *

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

def main():
    link_node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    image_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")

    link_html = textnode_to_htmlnode(link_node)
    image_html = textnode_to_htmlnode(image_node)

    print(repr(link_html))
    print(repr(image_html))

main()