import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "www.boot.dev", [], {"href": "https://www.boot.dev/", "target": "_blank"})
        result = node.props_to_html()
        expected = ' href="https://www.boot.dev/" target="_blank"'
        self.assertEqual(result, expected)

    def test_repr(self):
        node = HTMLNode("a", "www.boot.dev", [HTMLNode("b"), HTMLNode("c")], {"href": "https://www.boot.dev/", "target": "_blank"})
        expected = "HTMLNode('a', 'www.boot.dev', [HTMLNode('b'), HTMLNode('c')], {'href': 'https://www.boot.dev/', 'target': '_blank'})"
        self.assertEqual(repr(node), expected)

    def test_repr2(self):
        node = HTMLNode("a", "www.boot.dev", [HTMLNode("b"), HTMLNode("c"), HTMLNode("d", "www.google.com")], {"href": "https://www.boot.dev/", "target": "_blank", "money": "zero"})
        expected = "HTMLNode('a', 'www.boot.dev', [HTMLNode('b'), HTMLNode('c'), HTMLNode('d', 'www.google.com')], {'href': 'https://www.boot.dev/', 'target': '_blank', 'money': 'zero'})"
        self.assertEqual(repr(node), expected)