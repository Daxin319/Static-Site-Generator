import unittest

from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_props_to_html(self):
        node = LeafNode("a", "www.boot.dev", {"href": "https://www.boot.dev/", "target": "_blank"})
        result = node.props_to_html()
        expected = ' href="https://www.boot.dev/" target="_blank"'
        self.assertEqual(result, expected)

    def test_to_html(self):
        node = LeafNode("a", "www.boot.dev", {"href": "https://www.boot.dev/"})
        expected = '<a href="https://www.boot.dev/">www.boot.dev</a>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html2(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)