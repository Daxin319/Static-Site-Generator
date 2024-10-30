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

    def test_multiple_delimiters_bold_italic(self):
        # Test both bold (*) and italic (_) delimiters in one node, without nesting
        nodes = [TextNode("This is *bold* and _italic_ text.", TextType.TEXT)]
        
        # Split bold first, then italic
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        
        expected = [
            TextNode("This is "),
            TextNode("bold", TextType.BOLD),
            TextNode(" and "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.")
        ]
        self.assertEqual(result, expected)

    def test_code_and_bold_delimiters(self):
        # Test both code (`) and bold (*) delimiters in one node, without nesting
        nodes = [TextNode("Sample *bold* and `code` here.", TextType.TEXT)]
        
        # Split bold first, then code
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        result = split_nodes_delimiter(result, "`", TextType.CODE)
        
        expected = [
            TextNode("Sample "),
            TextNode("bold", TextType.BOLD),
            TextNode(" and "),
            TextNode("code", TextType.CODE),
            TextNode(" here.")
        ]
        self.assertEqual(result, expected)

    def test_italic_code_bold_order(self):
        # Test sequence of italic, code, and bold delimiters without nesting
        nodes = [TextNode("Try _italic_ `code` and *bold*.", TextType.TEXT)]
        
        # Split italic, then code, then bold
        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        result = split_nodes_delimiter(result, "`", TextType.CODE)
        result = split_nodes_delimiter(result, "*", TextType.BOLD)
        
        expected = [
            TextNode("Try "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" "),
            TextNode("code", TextType.CODE),
            TextNode(" and "),
            TextNode("bold", TextType.BOLD),
            TextNode(".")
        ]
        self.assertEqual(result, expected)

    def test_single_delimiter_with_text_only(self):
        # Test a single delimiter of each type in separate text to confirm splitting
        nodes = [
            TextNode("Single *bold* example.", TextType.TEXT),
            TextNode("Single _italic_ example.", TextType.TEXT),
            TextNode("Single `code` example.", TextType.TEXT)
        ]
        
        # Apply each delimiter type in sequence
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        result = split_nodes_delimiter(result, "`", TextType.CODE)
        
        expected = [
            TextNode("Single "),
            TextNode("bold", TextType.BOLD),
            TextNode(" example."),
            TextNode("Single "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" example."),
            TextNode("Single "),
            TextNode("code", TextType.CODE),
            TextNode(" example.")
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()