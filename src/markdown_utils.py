import re

from enum import Enum
from node_utils import text_to_textnodes
from htmlnode import ParentNode, LeafNode


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
    lines = [line.lstrip() for line in block.split("\n")]

    # If block is empty, treat as paragraph
    if not lines or all(line == "" for line in lines):
        return BlockType.PARAGRAPH

    if lines[0].startswith("#"):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif lines:
        is_quote = True
        for line in lines:
            if not (line.startswith(">") or line == ""):
                is_quote = False
                break
        if is_quote and any(line.startswith(">") for line in lines):
            return BlockType.QUOTE

        is_unordered = True
        for line in lines:
            if not (line.startswith("- ") or line == ""):
                is_unordered = False
                break
        # Only treat as unordered list if at least one line starts with "- "
        if is_unordered and any(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST

        is_ordered = True
        for line in lines:
            if not (re.match(r"^\d+\.\s", line) or line == ""):
                is_ordered = False
                break
        # Only treat as ordered list if at least one line matches ordered pattern
        if is_ordered and any(re.match(r"^\d+\.\s", line) for line in lines):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_content(block):
    """
    Convert a markdown block to its content.
    """
    if block.startswith("#"):
        return block[block.index(" ") + 1 :]
    elif block.startswith("```") and block.endswith("```"):
        return block[3:-3].lstrip("\n")
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
        return " ".join(block.splitlines()).strip()


def text_to_children(text):
    """
    Convert a markdown text to its children.
    """
    content = block_to_content(text)
    text_nodes = text_to_textnodes(content)
    html_nodes = [node.text_node_to_html_node() for node in text_nodes]
    return html_nodes


def markdown_to_html_node(markdown: str):
    html_nodes = []
    for md_block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(md_block)

        if block_type == BlockType.HEADING:
            heading_level = md_block.count("#", 0, md_block.find(" "))
            if heading_level < 1 or heading_level > 6:
                raise ValueError("Invalid heading level")
            html_nodes.append(
                ParentNode(
                    tag=f"h{heading_level}",
                    children=text_to_children(md_block),
                )
            )
        elif block_type == BlockType.CODE:
            content = block_to_content(md_block)
            html_nodes.append(
                ParentNode(
                    tag="pre",
                    children=[
                        LeafNode(tag="code", value=content),
                    ],
                )
            )
        elif block_type == BlockType.QUOTE:
            html_nodes.append(
                ParentNode(
                    tag="blockquote",
                    children=text_to_children(md_block),
                )
            )
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in md_block.split("\n"):
                line = line.strip()
                if line.startswith("- "):
                    content = line[2:].strip()
                    children = [
                        node.text_node_to_html_node()
                        for node in text_to_textnodes(content)
                    ]
                    items.append(ParentNode(tag="li", children=children))
            html_nodes.append(ParentNode(tag="ul", children=items))
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in md_block.split("\n"):
                line = line.strip()
                match = re.match(r"^\d+\.\s+(.*)", line)
                if match:
                    content = match.group(1).strip()
                    children = [
                        node.text_node_to_html_node()
                        for node in text_to_textnodes(content)
                    ]
                    items.append(ParentNode(tag="li", children=children))
            html_nodes.append(ParentNode(tag="ol", children=items))
        elif block_type == BlockType.PARAGRAPH:
            html_nodes.append(
                ParentNode(
                    tag="p",
                    children=text_to_children(md_block),
                )
            )
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode(tag="div", children=html_nodes)


def extract_title(markdown: str):
    """
    Extract the title from the markdown text.
    """
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block.split("\n")[0][2:]
    return None
