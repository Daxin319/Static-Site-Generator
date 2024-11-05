import unittest
from funcs import *

class TestFuncs(unittest.TestCase):
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

    def test_extract_markdown_images_single_image(self):
        # Test single image in markdown
        text = "This is an image ![alt text](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_multiple_images(self):
        # Test multiple images in markdown
        text = "First image ![image1](https://example.com/1.jpg) and second image ![image2](https://example.com/2.jpg)"
        result = extract_markdown_images(text)
        expected = [
            ("image1", "https://example.com/1.jpg"),
            ("image2", "https://example.com/2.jpg")
        ]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_no_image(self):
        # Test no image in markdown
        text = "This text has no image."
        result = extract_markdown_images(text)
        expected = []
        self.assertEqual(result, expected)
    
    def test_extract_markdown_images_edge_cases(self):
        # Test edge cases with empty alt text and url
        text = "Empty alt text ![](https://example.com/1.jpg) and empty URL ![image]()."
        result = extract_markdown_images(text)
        expected = [
            ("", "https://example.com/1.jpg"),
            ("image", "")
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_single_link(self):
        # Test single link in markdown
        text = "This is a [link](https://example.com)."
        result = extract_markdown_links(text)
        expected = [("link", "https://example.com")]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple_links(self):
        # Test multiple links in markdown
        text = "First [link1](https://example.com/1) and second [link2](https://example.com/2)"
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2")
        ]
        self.assertEqual(result, expected)
    
    def test_extract_markdown_links_no_links(self):
        # Test no link in markdown
        text = "This text has no link."
        result = extract_markdown_links(text)
        expected = []
        self.assertEqual(result, expected)

    def test_extract_markdown_links_edge_cases(self):
        # Test edge cases with empty alt text and url
        text = "Empty alt text []() and empty URL [link]()."
        result = extract_markdown_links(text)
        expected = [
            ("", ""),
            ("link", "")
        ]
        self.assertEqual(result, expected)

    def test_extract_images_and_links_mixed_content(self):
        # Test text with both images and links
        text = "Image here ![img](https://example.com/image.jpg) and a [link](https://example.com)"
        image_result = extract_markdown_images(text)
        link_result = extract_markdown_links(text)
        expected_images = [("img", "https://example.com/image.jpg")]
        expected_links = [("link", "https://example.com")]
        self.assertEqual(image_result, expected_images)
        self.assertEqual(link_result, expected_links)

    def test_split_nodes_image_single_image(self):
        # Test a single image within a node
        nodes = [TextNode("Here is an image ![alt text](https://example.com/image.jpg)")]
        result = split_nodes_image(nodes)
        
        expected = [
            TextNode("Here is an image "),
            TextNode("![alt text](https://example.com/image.jpg)", TextType.IMAGE)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_images(self):
        # Test multiple images within a node
        nodes = [TextNode("Image one ![img1](https://example.com/1.jpg) and image two ![img2](https://example.com/2.jpg)")]
        result = split_nodes_image(nodes)
        
        expected = [
            TextNode("Image one "),
            TextNode("![img1](https://example.com/1.jpg)", TextType.IMAGE),
            TextNode(" and image two "),
            TextNode("![img2](https://example.com/2.jpg)", TextType.IMAGE)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_images(self):
        # Test text with no images
        nodes = [TextNode("This text has no images.")]
        result = split_nodes_image(nodes)
        
        expected = [
            TextNode("This text has no images.")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_single_link(self):
        # Test a single link within a node
        nodes = [TextNode("This is a [link](https://example.com).")]
        result = split_nodes_link(nodes)
        
        expected = [
            TextNode("This is a "),
            TextNode("[link](https://example.com)", TextType.LINK),
            TextNode(".")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_links(self):
        # Test multiple links within a node
        nodes = [TextNode("First [link1](https://example.com/1) and second [link2](https://example.com/2)")]
        result = split_nodes_link(nodes)
        
        expected = [
            TextNode("First "),
            TextNode("[link1](https://example.com/1)", TextType.LINK),
            TextNode(" and second "),
            TextNode("[link2](https://example.com/2)", TextType.LINK)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        # Test text with no links
        nodes = [TextNode("This text has no links.")]
        result = split_nodes_link(nodes)
        
        expected = [
            TextNode("This text has no links.")
        ]
        self.assertEqual(result, expected)
    
    def test_split_nodes_image_and_link_combined(self):
        # Test node with both images and links
        nodes = [TextNode("Here is an image ![img](https://example.com/image.jpg) and a [link](https://example.com).")]
        
        result_images = split_nodes_image(nodes)
        result_links = split_nodes_link(result_images)
        
        expected = [
            TextNode("Here is an image "),
            TextNode("![img](https://example.com/image.jpg)", TextType.IMAGE),
            TextNode(" and a "),
            TextNode("[link](https://example.com)", TextType.LINK),
            TextNode(".")
        ]
        self.assertEqual(result_links, expected)
        
    def test_split_nodes_image_empty_alt_text_exception(self):
        # Test image with an empty alt text should raise an exception
        nodes = [TextNode("Image with no alt text ![](https://example.com/image.jpg)")]
        with self.assertRaises(Exception) as context:
            split_nodes_image(nodes)
        self.assertEqual(str(context.exception), '<----------------Alt Text is empty---------------->')

    def test_split_nodes_image_empty_url_exception(self):
        # Test image with an empty URL should raise an exception
        nodes = [TextNode("Image with empty URL ![alt text]()")]
        with self.assertRaises(Exception) as context:
            split_nodes_image(nodes)
        self.assertEqual(str(context.exception), '<----------------No URL Detected---------------->')

    def test_split_nodes_link_empty_link_text_exception(self):
        # Test link with an empty link text should raise an exception
        nodes = [TextNode("Link with no text []()")]
        with self.assertRaises(Exception) as context:
            split_nodes_link(nodes)
        self.assertEqual(str(context.exception), '<----------------Link is empty---------------->')

    def test_split_nodes_link_empty_url_exception(self):
        # Test link with an empty URL should raise an exception
        nodes = [TextNode("Link with empty URL [link]()")]
        with self.assertRaises(Exception) as context:
            split_nodes_link(nodes)
        self.assertEqual(str(context.exception), '<----------------No URL Detected---------------->')

    def test_split_nodes_image_and_link_no_exceptions_for_valid_input(self):
        # Test valid images and links to ensure no exceptions are raised
        nodes = [TextNode("Valid image ![alt](https://example.com/image.jpg) and link [link](https://example.com).")]
        try:
            result_images = split_nodes_image(nodes)
            result_links = split_nodes_link(result_images)
            self.assertIsInstance(result_links, list)  # Ensure it returns a list
        except Exception as e:
            self.fail(f"An exception was raised for valid input: {e}")

if __name__ == '__main__':
    unittest.main()