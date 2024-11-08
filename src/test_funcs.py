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
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.jpg")
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_images(self):
        # Test multiple images within a node
        nodes = [TextNode("Image one ![img1](https://example.com/1.jpg) and image two ![img2](https://example.com/2.jpg)")]
        result = split_nodes_image(nodes)
        
        expected = [
            TextNode("Image one "),
            TextNode("img1", TextType.IMAGE, "https://example.com/1.jpg"),
            TextNode(" and image two "),
            TextNode("img2", TextType.IMAGE, "https://example.com/2.jpg")
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
        input_nodes = [TextNode("This is a [link](https://example.com).")]
        expected = [
            TextNode("This is a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT, None)
        ]
        result = split_nodes_link(input_nodes)
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_links(self):
        input_nodes = [TextNode("First [link1](https://example.com/1) and second [link2](https://example.com/2).")]
        expected = [
            TextNode("First ", TextType.TEXT, None),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" and second ", TextType.TEXT, None),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
            TextNode(".", TextType.TEXT, None)
        ]
        result = split_nodes_link(input_nodes)
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
        input_nodes = [
            TextNode("Here is an image ![img](https://example.com/image.jpg) and a [link](https://example.com).")
        ]
        expected = [
            TextNode("Here is an image ", TextType.TEXT, None),
            TextNode("img", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(" and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT, None)
        ]
        result = split_nodes_link(split_nodes_image(input_nodes))
        self.assertEqual(result, expected)

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

    def test_text_with_plain_text(self):
        # Test plain text without any formatting
        result = text_to_textnodes("This is plain text.")
        expected = [TextNode("This is plain text.")]
        self.assertEqual(result, expected)

    def test_text_with_single_link(self):
        input_nodes = [TextNode("Here is a [link](https://example.com).")]
        expected = [
            TextNode("Here is a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT, None)
        ]
        result = split_nodes_link(input_nodes)
        self.assertEqual(result, expected)

    def test_text_with_single_image(self):
        # Test text with a single markdown image
        result = text_to_textnodes("Here is an image ![alt](https://example.com/image.jpg).")
        expected = [
            TextNode("Here is an image "),
            TextNode("alt", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(".")
        ]
        self.assertEqual(result, expected)

    def test_text_with_bold_and_italic(self):
        # Test text with bold and italic separately
        result = text_to_textnodes("This is **bold** and *italic* text.")
        expected = [
            TextNode("This is "),
            TextNode("bold", TextType.BOLD),
            TextNode(" and "),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.")
        ]
        self.assertEqual(result, expected)

    def test_text_with_inline_code(self):
        # Test text with inline code
        result = text_to_textnodes("Here is `inline code`.")
        expected = [
            TextNode("Here is "),
            TextNode("inline code", TextType.CODE),
            TextNode(".")
        ]
        self.assertEqual(result, expected)

    def test_text_with_multiple_formatting_no_nesting(self):
        input_text = "This includes **bold**, *italic*, `code`, and a [link](https://example.com)."
        expected = [
            TextNode("This includes ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(", ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(", ", TextType.TEXT, None),
            TextNode("code", TextType.CODE, None),
            TextNode(", and a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT, None)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)

    def test_text_with_unclosed_bold_delimiter(self):
        # Test case with missing closing delimiter for bold text
        with self.assertRaises(Exception) as context:
            text_to_textnodes("This is **bold text without closing.")
        self.assertIn("Invalid markdown syntax", str(context.exception))

    def test_basic_markdown(self):
        """Test markdown with heading, paragraph, and list."""
        markdown = """# Heading

This is a paragraph with **bold** and *italic* text.

* Item 1
* Item 2"""
        expected = [
            "# Heading",
            "This is a paragraph with **bold** and *italic* text.",
            "* Item 1\n* Item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_empty_input(self):
        """Test empty input raises an exception."""
        with self.assertRaises(Exception) as context:
            markdown_to_blocks("")
        self.assertEqual(str(context.exception), "<----------Empty document inputted---------->")
    
    def test_only_newlines(self):
        """Test input containing only newlines."""
        markdown = "\n\n\n"
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_multiple_empty_blocks(self):
        """Test markdown with multiple empty blocks."""
        markdown = """# Heading


This is a paragraph.


* List item 1
* List item 2"""
        expected = [
            "# Heading",
            "This is a paragraph.",
            "* List item 1\n* List item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_leading_and_trailing_spaces(self):
        """Test blocks with leading and trailing spaces."""
        markdown = """   # Heading    

   This is a paragraph with spaces.   

* Item 1  
* Item 2"""
        expected = [
            "# Heading",
            "This is a paragraph with spaces.",
            "* Item 1\n* Item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_single_block_no_double_newlines(self):
        """Test markdown with a single block and no double newlines."""
        markdown = "This is a single block without double newlines."
        expected = ["This is a single block without double newlines."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_mixed_content(self):
        """Test markdown with mixed content types, including headings and lists."""
        markdown = """# Heading

Paragraph with **bold** text.

# Another Heading

Another paragraph with *italic* text.

* List item 1
* List item 2"""
        expected = [
            "# Heading",
            "Paragraph with **bold** text.",
            "# Another Heading",
            "Another paragraph with *italic* text.",
            "* List item 1\n* List item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_trailing_newlines(self):
        """Test markdown with trailing newlines after the last block."""
        markdown = """# Heading

Paragraph.

* List item 1
* List item 2


"""
        expected = [
            "# Heading",
            "Paragraph.",
            "* List item 1\n* List item 2"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_unicode_characters(self):
        """Test markdown with Unicode characters."""
        markdown = """# Heading 🎉

Paragraph with emojis 🚀 and symbols ©.

* Emoji 😊
* Another item"""
        expected = [
            "# Heading 🎉",
            "Paragraph with emojis 🚀 and symbols ©.",
            "* Emoji 😊\n* Another item"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_with_links_and_images(self):
        """Test markdown containing links and images."""
        markdown = """# Heading

This is a paragraph with a [link](https://example.com) and an image ![alt text](https://example.com/image.jpg).

* List with [link](https://example.org)
* List with image ![image](https://example.org/image.png)"""
        expected = [
            "# Heading",
            "This is a paragraph with a [link](https://example.com) and an image ![alt text](https://example.com/image.jpg).",
            "* List with [link](https://example.org)\n* List with image ![image](https://example.org/image.png)"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)


    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("###### Heading 6"), "heading")
        self.assertEqual(block_to_block_type("#### Mid-Level Heading"), "heading")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('Hello World')\n```"), "code")
        self.assertEqual(block_to_block_type("```\nint x = 5;\nint y = 10;\n```"), "code")

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote\n> with multiple lines"), "quote")
        self.assertEqual(block_to_block_type("> Single line quote"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2\n* Item 3"), "unordered_list")
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), "unordered_list")
        self.assertEqual(block_to_block_type("* Mixed types\n- still unordered"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item\n3. Third item"), "ordered_list")
        self.assertEqual(block_to_block_type("1. Step one\n2. Step two\n3. Step three"), "ordered_list")

    def test_invalid_ordered_list(self):
        # Not starting at 1
        self.assertEqual(block_to_block_type("2. Wrong start\n3. Skipped one"), "paragraph")
        # Incorrectly incremented numbers
        self.assertEqual(block_to_block_type("1. Right start\n3. Skips second\n4. Wrong sequence"), "paragraph")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a regular paragraph of text."), "paragraph")
        self.assertEqual(block_to_block_type("No special formatting here.\nJust a normal block of text."), "paragraph")

    def test_heading_conversion(self):
        result = markdown_to_html_node("# Heading 1")
        expected = HTMLNode("div", None, [HTMLNode("h1", None, [LeafNode(None, "Heading 1")])])
        self.assertEqual(result, expected)

        result = markdown_to_html_node("### Heading 3")
        expected = HTMLNode("div", None, [HTMLNode("h3", None, [LeafNode(None, "Heading 3")])])
        self.assertEqual(result, expected)

    def test_paragraph_conversion(self):
        result = markdown_to_html_node("This is a paragraph.")
        expected = HTMLNode("div", None, [HTMLNode("p", None, [LeafNode(None, "This is a paragraph.")])])
        self.assertEqual(result, expected)

    def test_code_block_conversion(self):
        result = markdown_to_html_node("```\nprint('Hello')\n```")
        expected = HTMLNode("div", None, [HTMLNode("pre", None, [LeafNode("code", "print('Hello')")])])
        self.assertEqual(result, expected)

    def test_quote_block_conversion(self):
        result = markdown_to_html_node("> This is a quote.")
        expected = HTMLNode("div", None, [HTMLNode("blockquote", None, [LeafNode(None, "This is a quote.")])])
        self.assertEqual(result, expected)

    def test_unordered_list_conversion(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        result = markdown_to_html_node(markdown)
        expected = HTMLNode("div", None, [
            HTMLNode("ul", None, [
                HTMLNode("li", None, [LeafNode(None, "Item 1")]),
                HTMLNode("li", None, [LeafNode(None, "Item 2")]),
                HTMLNode("li", None, [LeafNode(None, "Item 3")])
            ])
        ])
        self.assertEqual(result, expected)

    def test_ordered_list_conversion(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        result = markdown_to_html_node(markdown)
        expected = HTMLNode("div", None, [
            HTMLNode("ol", None, [
                HTMLNode("li", None, [LeafNode(None, "First item")]),
                HTMLNode("li", None, [LeafNode(None, "Second item")]),
                HTMLNode("li", None, [LeafNode(None, "Third item")])
            ])
        ])
        self.assertEqual(result, expected)

    def test_combination_of_blocks(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n> A quote.\n\n* List item 1\n* List item 2"
        result = markdown_to_html_node(markdown)
        expected = HTMLNode("div", None, [
            HTMLNode("h1", None, [LeafNode(None, "Heading")]),
            HTMLNode("p", None, [LeafNode(None, "This is a paragraph.")]),
            HTMLNode("blockquote", None, [LeafNode(None, "A quote.")]),
            HTMLNode("ul", None, [
                HTMLNode("li", None, [LeafNode(None, "List item 1")]),
                HTMLNode("li", None, [LeafNode(None, "List item 2")])
            ])
        ])
        self.assertEqual(result, expected)

    def test_text_formatting(self):
        markdown = "This text is **bold** and *italic* with `code`."
        result = markdown_to_html_node(markdown)
        expected = HTMLNode("div", None, [
            HTMLNode("p", None, [
                LeafNode(None, "This text is "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " with "),
                LeafNode("code", "code"),
                LeafNode(None, ".")
            ])
        ])
        self.assertEqual(result, expected)

    def test_mixed_inline_elements(self):
        input_text = "This includes **bold** text, *italic* text, `code`, a [link](https://example.com), and an image ![alt](https://example.com/image.jpg)."
        expected = [
            TextNode("This includes ", TextType.TEXT, None),
            TextNode("bold", TextType.BOLD, None),
            TextNode(" text, ", TextType.TEXT, None),
            TextNode("italic", TextType.ITALIC, None),
            TextNode(" text, ", TextType.TEXT, None),
            TextNode("code", TextType.CODE, None),
            TextNode(", a ", TextType.TEXT, None),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(", and an image ", TextType.TEXT, None),
            TextNode("alt", TextType.IMAGE, "https://example.com/image.jpg"),
            TextNode(".", TextType.TEXT, None)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqual(result, expected)
        
    def test_valid_h1_heading(self):
        markdown = "# This is a Title\nSome other text."
        expected = "This is a Title"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_no_h1_heading(self):
        markdown = "This is some text without an H1 heading."
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "<----------No H1 Heading Found---------->")

    def test_h1_with_leading_and_trailing_whitespace(self):
        markdown = "#    Title with Spaces    \nAnother line of text."
        expected = "Title with Spaces"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_h1_heading_in_middle_of_text(self):
        markdown = "Intro text\n# Middle Heading\nMore text below."
        expected = "Middle Heading"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_multiple_h1_headings(self):
        markdown = "# First Title\nSome text.\n# Second Title"
        expected = "First Title"  # Only the first H1 should be extracted.
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_h1_heading_with_special_characters(self):
        markdown = "# Title with !@#$%^&*() Special Characters"
        expected = "Title with !@#$%^&*() Special Characters"
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_empty_input(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "<----------No H1 Heading Found---------->")

    def test_h1_heading_but_not_first_line(self):
        markdown = "Some text\n\n# Actual Title\nMore content."
        expected = "Actual Title"
        result = extract_title(markdown)
        self.assertEqual(result, expected)




if __name__ == '__main__':
    unittest.main()