import re

from textnode import TextNode, TextType


def split_nodes_delimiter(nodes, delimiter, new_type):
    result = []
    for node in nodes:
        if not isinstance(node, TextNode):
            raise TypeError("Expected a TextNode")

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
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise TypeError("Expected a TextNode")

        text = node.text if node.text is not None else ""
        images = extract_markdown_images(text)
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Image section is not closed, please check!")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            if text := sections[1] != "":
                new_nodes.append(TextNode(text))


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise TypeError("Expected a TextNode")

        text = node.text if node.text is not None else ""
        links, pattern = extract_markdown_links(text)
        split_text = re.split(pattern, text)
        if not links:
            new_nodes.append(node)
            continue
        for i, part in enumerate(split_text):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, node.text_type))
            else:
                text, url = links[i // 2]
                new_nodes.append(TextNode(part, TextType.LINK, text, url))
