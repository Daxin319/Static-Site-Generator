import unittest

from parentnode import *
from leafnode import *

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

        # Test with an empty children list
    def test_empty_children(self):
        node = ParentNode("div", [])
        expected = "<div></div>"
        self.assertEqual(node.to_html(), expected)

    # Test for missing tag (should raise ValueError)
    def test_missing_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "Some text")]).to_html()

    # Test for invalid children type (should raise ValueError)
    def test_invalid_children_type(self):
        with self.assertRaises(ValueError):
            ParentNode("div", "Not a list")

    # Test to_html with props (assuming props_to_html is correctly implemented in HTMLNode)
    def test_to_html_with_props(self):
        node = ParentNode("p", [LeafNode(None, "Text")], props={"class": "my-class"})
        expected = '<p class="my-class">Text</p>'
        self.assertEqual(node.to_html(), expected)