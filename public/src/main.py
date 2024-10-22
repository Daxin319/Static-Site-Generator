from textnode import *
from parentnode import *
from leafnode import *
from htmlnode import *

def main():
    link_node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    image_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")

    link_html = textnode_to_htmlnode(link_node)
    image_html = textnode_to_htmlnode(image_node)

    print(repr(link_html))
    print(repr(image_html))

main()