import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    # test eq func with matching inputs
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    #test eq func with different inputs
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    #make sure code handles None inputs correctly
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    #test if code sees typos
    def test_eq4(self):
        node = TextNode("This is aa text node", TextType.BOLD)
        node2 = TextNode("This is a text nodee", TextType.BOLD)
        self.assertNotEqual(node, node2)

    #test url attribute
    def test_eq5(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        self.assertEqual(node, node2)

    # test missing url
    def test_eq6(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    #test url typos
    def test_eq7(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev/")
        self.assertNotEqual(node, node2)    

    def test_text_conversion(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = textnode_to_htmlnode(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_bold_conversion(self):
        bold_node = TextNode("Bold text", TextType.BOLD)
        html_node = textnode_to_htmlnode(bold_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_conversion(self):
        italic_node = TextNode("Italic text", TextType.ITALIC)
        html_node = textnode_to_htmlnode(italic_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_conversion(self):
        code_node = TextNode("print('Hello')", TextType.CODE)
        html_node = textnode_to_htmlnode(code_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_link_conversion(self):
        link_node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = textnode_to_htmlnode(link_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), '<a href="https://www.example.com">Click me</a>')

    def test_image_conversion(self):
        image_node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = textnode_to_htmlnode(image_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.jpg" alt="Alt text" />')

    def test_invalid_type_conversion(self):
        invalid_node = TextNode("Invalid", "INVALID_TYPE")
        with self.assertRaises(ValueError):
            textnode_to_htmlnode(invalid_node)
            
if __name__ == "__main__":
    unittest.main()