from textnode import *
import re


# function to convert raw markdown to list of TextNodes, takes list as input.        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT :
            new_nodes.append(node)
        else:
            first_pos = node.text.find(delimiter) #find first delimiter
            second_pos = node.text.find(delimiter, first_pos + 1)
            if second_pos == -1 and first_pos != -1:
                raise Exception('<----------------------Invalid markdown syntax, no closing delimiter found or empty set of delimiters found---------------------->')
            if first_pos == -1:
                new_nodes.append(TextNode(node.text))
            else:
                if node.text[:first_pos]:
                    new_nodes.append(TextNode(node.text[:first_pos]))
                new_nodes.append(TextNode(node.text[first_pos + len(delimiter):second_pos], text_type))
                if node.text[second_pos + len(delimiter):]:
                    new_nodes.extend(split_nodes_delimiter([TextNode(node.text[second_pos + len(delimiter):])], delimiter, text_type))
    return new_nodes

# function to convert raw markdown text to a list of tuples. Each tuple contains the alt text and url of markdown images.
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#function to covert raw markdown text to a list of tuples. Each tuple contains the alt text and url of markdown links.
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#function to split image nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        list = extract_markdown_images(node.text)
        if len(list) == 0:
            new_nodes.append(node)
        else:
            for alt_text, url in list:
                if len(alt_text) == 0:
                    raise Exception('<----------------Alt Text is empty---------------->')
                if len(url) == 0:
                    raise Exception('<----------------No URL Detected---------------->')
                split_text = node.text.split(f'![{alt_text}]({url})', 1)
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], node.text_type))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                node.text = split_text[1]
            if len(node.text) != 0:
                new_nodes.append(TextNode(node.text)) 
    return new_nodes

#function to split link nodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        list = extract_markdown_links(node.text)
        if len(list) == 0:
            new_nodes.append(node)
        else:
            for link_text, url in list:
                if len(link_text) == 0:
                    raise Exception('<----------------Link is empty---------------->')
                if len(url) == 0:
                    raise Exception('<----------------No URL Detected---------------->')
                split_text = node.text.split(f'[{link_text}]({url})', 1)
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], node.text_type))
                new_nodes.append(TextNode(link_text, TextType.LINK, url))
                node.text = split_text[1]
            if len(node.text) != 0:
                new_nodes.append(TextNode(node.text, node.text_type))        
    return new_nodes

# This function takes raw markdown text and converts it into a list of textnodes
def text_to_textnodes(text):
    node = TextNode(text)
    code = split_nodes_delimiter([node], '`', TextType.CODE)
    bold = split_nodes_delimiter(code, '**', TextType.BOLD)
    italic = split_nodes_delimiter(bold, '*', TextType.ITALIC)
    images = split_nodes_image(italic)
    links = split_nodes_link(images)
    return links


# This function converts raw markdown text into blocks. Input raw markdown string and output list of block strings.
def markdown_to_blocks(markdown):
    if markdown:
        nline_split = markdown.split('\n\n')
        new_list = []
        for line in nline_split:
            if len(line) == 0 or line == "\n":
                pass
            stripped_line = line.strip(' \n')
            if len(stripped_line) != 0:
                new_list.append(stripped_line)
        return new_list
    raise Exception("<----------Empty document inputted---------->")

# This funciton takes an input of a single block of markdown text and returns a string describing  the type of block it is
def block_to_block_type(markdown):
    is_heading = re.search(r"^#{1,6}\s", markdown)
    is_code = re.search(r"(^`{3})[\s\S]*(`{3}$)", markdown)
    is_quote = re.search(r"^>", markdown, flags= re.MULTILINE)
    is_unordered_list1 = re.search(r"^\*\s", markdown, flags= re.MULTILINE)
    is_unordered_list2 = re.search(r"^-\s", markdown, flags= re.MULTILINE)
    is_ordered_list = re.search(r"^(\d+)\.\s+", markdown, flags= re.MULTILINE)

    if is_heading:
        return "heading"
    if is_code:
        return "code"
    if is_quote:
        return "quote"
    if is_unordered_list1 or is_unordered_list2:
        return "unordered_list"
    if is_ordered_list:
        split_text = markdown.split('\n')
        current_index = 0
        for line in split_text:
            match = re.match(r"^(\d+)\.\s+", line)
            if match:
                num = match.group(1)
                if int(num) != current_index + 1:
                    return "paragraph"
                current_index += 1
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                matching = re.match(r"(^#{1,6})", block)
                group = matching.group(1)
                num = len(group)
                stripped = block.lstrip("# ")
                converted = text_to_children(stripped)
                node = HTMLNode(f"h{num}", None, converted)
                block_nodes.append(node)
            case "code":
                stripped = block.lstrip("`\n ").rstrip("`\n ")
                child_node = HTMLNode("code", stripped)
                node = HTMLNode("pre", None, [child_node])
                block_nodes.append(node)
            case "quote":
                stripped = block.lstrip("> ")
                converted = text_to_children(stripped)
                node = HTMLNode("blockquote", None, converted)
                block_nodes.append(node)
            case "unordered_list":
                list_items = []
                split_block = block.split("\n")
                for item in split_block:
                    stripped = item.lstrip("*- ")
                    converted = text_to_children(stripped)
                    node = HTMLNode("li", None, converted)
                    list_items.append(node)
                parent_node = HTMLNode("ul", None, list_items)
                block_nodes.append(parent_node)
            case "ordered_list":
                list_items = []
                split_block = block.split("\n")
                for item in split_block:
                    match = re.match(r"^(\d+\.\s+)", item)
                    num = match.group(1)
                    stripped = item.lstrip(num)
                    converted = text_to_children(stripped)
                    node = HTMLNode("li", None, converted)
                    list_items.append(node)
                parent_node = HTMLNode("ol", None, list_items)
                block_nodes.append(parent_node)
            case "paragraph":
                converted = text_to_children(block)
                node = HTMLNode("p", None, converted)
                block_nodes.append(node)
    return HTMLNode("div", None, block_nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        new_node = textnode_to_htmlnode(node)
        html_nodes.append(new_node)
    return html_nodes


test_text = "This is a [link](http://example.com) and this is **bold with a [second link](http://test.com)**"
test_node = TextNode(test_text, TextType.BOLD)
result = split_nodes_link([test_node])
print("Test results:", [(node.text, node.text_type) for node in result])