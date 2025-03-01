import re
import os
import shutil
from textnode import *



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
    italic = split_nodes_delimiter(bold, '_', TextType.ITALIC)
    images = split_nodes_image(italic)
    links = split_nodes_link(images)
    return links


# This function converts raw markdown text into blocks. Input raw markdown string and output list of block strings.
def markdown_to_blocks(markdown):
    if not markdown:
        raise Exception("<----------Empty document inputted---------->")
    
    lines = markdown.split('\n')
    blocks = []
    current_block = []
    in_code_block = False
    
    for line in lines:
        # Check for code fence
        if line.strip().startswith('```'):
            if not in_code_block:
                # Starting a new code block
                in_code_block = True
                current_block = [line]
            else:
                # Ending a code block
                current_block.append(line)
                blocks.append('\n'.join(current_block))
                current_block = []
                in_code_block = False
            continue
            
        if in_code_block:
            # If we're in a code block, add all lines
            current_block.append(line)
        else:
            # Normal block processing
            if line.strip():
                current_block.append(line.strip())
            elif current_block:
                blocks.append('\n'.join(current_block).strip())
                current_block = []
    
    # Don't forget any remaining content
    if current_block:
        if in_code_block:
            blocks.append('\n'.join(current_block))
        else:
            blocks.append('\n'.join(current_block).strip())
    
    return blocks

# This funciton takes an input of a single block of markdown text and returns a string describing  the type of block it is
def block_to_block_type(markdown):
    is_heading = re.search(r"^#{1,6}\s", markdown)
    is_code = re.search(r"^```[\s\S]*```$", markdown, re.MULTILINE)
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
                stripped = block.replace('```', '').strip()
                content = stripped.split('\n')
                code_content = '\n'.join(content)
                child_node = HTMLNode("code", code_content)
                node = HTMLNode("pre", None, [child_node])
                block_nodes.append(node)
            case "quote":
                stripped = block.replace("> ", "")
                converted = text_to_children(stripped)
                node = HTMLNode("blockquote", None, converted)
                block_nodes.append(node)
            case "unordered_list":
                list_items = []
                split_block = block.split("\n")
                for item in split_block:
                    stripped = item.lstrip('-*').lstrip()
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


# Function to transfer files from one location to another. written recursively as practice, I know I could just use shutil.copytree
def file_transfer(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)
    transfer_helper(source, destination)

def transfer_helper(source, destination):
    file_list = os.listdir(source)
    for item in file_list:
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            transfer_helper(src_path, dst_path)

def extract_title(markdown):
    split_file = markdown.split("\n")
    for line in split_file:
        if line.startswith("# "):
            stripped = line.lstrip("# ").rstrip(" ")
            return stripped
    raise Exception("<----------No H1 Heading Found---------->")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"<------------------------------------Generating page from {from_path} to {dest_path} using template from {template_path}------------------------------------>")
    dst_dir = os.path.dirname(dest_path)

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    with open(from_path, 'r', encoding="utf-8") as file:
        file_string = file.read()
        html_node = markdown_to_html_node(file_string)
        title = extract_title(file_string)
        content_string = html_node.to_html()

    with open(template_path, 'r', encoding="utf-8") as template:
        template_string = template.read()
        template_string = template_string.replace("{{ Title }}", title).replace("{{ Content }}", content_string)
        replaced_template = template_string.replace("href=\"/", "href=\"" + basepath).replace("src=\"/", "src=\"" + basepath)

    with open(dest_path, 'w', encoding="utf-8") as result:
        result.write(replaced_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        base_name, _ = os.path.splitext(item)
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        dest_file_path = os.path.join(dest_dir_path, base_name + '.html')

        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_file_path, basepath)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
