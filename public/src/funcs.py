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
            for item in list:
                alt_text = item[0]
                url = item[1]
                if len(alt_text) == 0:
                    raise Exception('<----------------Alt Text is empty---------------->')
                if len(url) == 0:
                    raise Exception('<----------------No URL Detected---------------->')
                split_text = node.text.split(f'![{alt_text}]({url})', 1)
                new_nodes.append(TextNode(split_text[0]))
                new_nodes.append(TextNode(f'![{alt_text}]({url})', TextType.IMAGE))
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
            for item in list:
                link = item[0]
                url = item[1]
                if len(link) == 0:
                    raise Exception('<----------------Link is empty---------------->')
                if len(url) == 0:
                    raise Exception('<----------------No URL Detected---------------->')
                split_text = node.text.split(f'[{link}]({url})', 1)
                new_nodes.append(TextNode(split_text[0]))
                new_nodes.append(TextNode(f'[{link}]({url})', TextType.LINK))
                node.text = split_text[1]
            if len(node.text) != 0:
                new_nodes.append(TextNode(node.text))        
    return new_nodes

# This function takes raw markdown text and converts it into a list of textnodes
def text_to_textnodes(text):
    node = TextNode(text)
    links = split_nodes_link([node])
    images = split_nodes_image(links)
    code = split_nodes_delimiter(images, '`', TextType.CODE)
    bold = split_nodes_delimiter(code, '**', TextType.BOLD)
    italic = split_nodes_delimiter(bold, '*', TextType.ITALIC)
    return italic
