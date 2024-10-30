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

if __name__ == "__main__":
    unittest.main()