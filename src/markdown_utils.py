import re

from enum import Enum
from node_utils import text_to_textnodes
from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    """
    Convert markdown text to a list of TextNode objects.
    """
    blocks = markdown.split("\n\n")
    blocks = [block.strip().strip(" ") for block in blocks if block.strip()]
    return blocks


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in block.split("\n"):
            if line.strip() and not line.startswith(">"):
                return BlockType.PARAGRAPH
            else:
                return BlockType.QUOTE
    elif block.startswith("- "):
        for line in block.split("\n"):
            if line.strip() and not line.startswith("- "):
                return BlockType.PARAGRAPH
            else:
                return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        for line in block.split("\n"):
            if line.strip() and not re.match(r"^\d+\.\s", line):
                return BlockType.PARAGRAPH
            else:
                return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def block_to_content(block):
    """
    Convert a markdown block to its content.
    """
    if block.startswith("#"):
        return block[block.index(" ") + 1 :]
    elif block.startswith("```") and block.endswith("```"):
        return block[3:-3].strip()
    elif block.startswith(">"):
        new_block = ""
        for line in block.split("\n"):
            if line.strip() and not line.startswith(">"):
                new_block += line.strip() + "\n"
            else:
                new_block += line[1:].strip() + "\n"
        return new_block.strip()
    elif block.startswith("- "):
        new_block = ""
        for line in block.split("\n"):
            if line.strip() and not line.startswith("- "):
                new_block += line.strip() + "\n"
            else:
                new_block += line[2:].strip() + "\n"
        return new_block.strip()
    elif block.startswith("1. "):
        new_block = ""
        for line in block.split("\n"):
            if line.strip() and not re.match(r"^\d+\.\s", line):
                new_block += line.strip() + "\n"
            else:
                new_block += line[line.index(".") + 1 :].strip() + "\n"
        return new_block.strip()
    else:
        return block.strip()

def markdown_to_html_node(markdown: str):
    html_nodes = []
    for md_block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(md_block)
        children = block_to_content(md_block)
        text_nodes = text_to_textnodes(children)
        leaf_nodes = [node.text_node_to_html_node() for node in text_nodes]

        if block_type == BlockType.HEADING:
            heading_level = md_block.count("#", 0, md_block.find(" "))
            if heading_level < 1 or heading_level > 6:
                raise ValueError("Invalid heading level")
            html_nodes.append(
                HTMLNode(
                    tag=f"h{heading_level}",
                    children=leaf_nodes,
                )
            )
        elif block_type == BlockType.CODE:
            html_nodes.append(
                HTMLNode(
                    tag="pre",
                    children=[
                        HTMLNode(
                            tag="code",
                            children=leaf_nodes,
                        )
                    ],
                )
            )
        elif block_type == BlockType.QUOTE:
            html_nodes.append(
                HTMLNode(
                    tag="blockquote",
                    children=leaf_nodes,
                )
            )
        elif block_type == BlockType.UNORDERED_LIST:
            items = [
                HTMLNode(tag="li", children=[item_node])
                for item_node in [HTMLNode(tag=None, children=[node]) for node in leaf_nodes]
            ]
            html_nodes.append(
                HTMLNode(
                    tag="ul",
                    children=items,
                )
            )
        elif block_type == BlockType.ORDERED_LIST:
            items = [
                HTMLNode(tag="li", children=[item_node])
                for item_node in [HTMLNode(tag=None, children=[node]) for node in leaf_nodes]
            ]
            html_nodes.append(
                HTMLNode(
                    tag="ol",
                    children=items,
                )
            )
        elif block_type == BlockType.PARAGRAPH:
            html_nodes.append(
                HTMLNode(
                    tag="p",
                    children=leaf_nodes,
                )
            )
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return html_nodes
