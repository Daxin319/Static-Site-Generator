import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is aa text node", TextType.BOLD)
        node2 = TextNode("This is a text nodee", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        self.assertEqual(node, node2)

    def test_eq6(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq7(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev/")
        self.assertNotEqual(node, node2)    



class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        # Text with a pair of delimiters
        nodes = [TextNode("Hello *world*!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        
        expected = [
            TextNode("Hello "),
            TextNode("world", TextType.BOLD),
            TextNode("!")
        ]
        self.assertEqual(result, expected)
    
    def test_no_delimiter_found(self):
        # Text without the delimiter should return original node
        nodes = [TextNode("Hello world!", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        
        expected = [TextNode("Hello world!", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_invalid_syntax_single_delimiter(self):
        # Single delimiter, should raise an exception
        nodes = [TextNode("Hello *world!", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)

    def test_nested_delimiter_split(self):
        # Nested delimiters, expecting recursive behavior
        nodes = [TextNode("Hello *world* and *everyone*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        
        expected = [
            TextNode("Hello "),
            TextNode("world", TextType.BOLD),
            TextNode(" and "),
            TextNode("everyone", TextType.BOLD)
        ]
        self.assertEqual(result, expected)
    
    def test_non_text_type_node(self):
        # Node is not of TextType.TEXT, should be returned unmodified
        non_text_node = HTMLNode("div", "Some content")
        result = split_nodes_delimiter([non_text_node], "*", TextType.BOLD)
        
        self.assertEqual(result, [non_text_node])

if __name__ == "__main__":
    unittest.main()