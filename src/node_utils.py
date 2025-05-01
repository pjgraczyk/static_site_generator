import re

from textnode import TextNode, TextType
from typing import List


def split_nodes_delimiter(nodes, delimiter, new_type):
    result = []
    for node in nodes:
        if not isinstance(node, TextNode):
            result.append(node)
            continue

        text = node.text if node.text is not None else ""

        parts = text.split(delimiter)

        if len(parts) == 1:
            result.append(node)
            continue
        elif len(parts) == 2:
            result.append(TextNode(parts[0], node.text_type))
            result.append(TextNode(parts[1], node.text_type))
            continue
        else:
            for i, part in enumerate(parts):
                if not part:
                    continue

                current_type = node.text_type if i % 2 == 0 else new_type
                result.append(TextNode(part, current_type))

    return result


def extract_markdown_images(text):
    regexp_image = r"!\[(.*?)\]\((.*?)\)"
    images = re.findall(regexp_image, text)
    return images


def extract_markdown_links(text):
    regexp_link = r"(?<!!)\[(.*?)\]\((.*?)\)"
    links = re.findall(regexp_link, text)
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    map = {
        TextType.BOLD: "**",
        TextType.CODE: "`",
        TextType.ITALIC: "*",
    }

    new_nodes = [TextNode(text, TextType.TEXT)]
    for text_type, delimiter in map.items():
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes
