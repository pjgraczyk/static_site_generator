import re

from enum import Enum
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

def markdown_to_html(markdown: str) -> str:
    md_blocks = markdown_to_blocks(markdown)
    md_blocks_types = []
    for block in md_blocks:
        block_type = block_to_block_type(block)
        md_blocks_types.append(block_type)
        
    ## TODO: Implement the conversion to TextNode, then convert it to HTMLNode
    text_nodes_dict = {}
    for md_block, block_type in zip(md_blocks, md_blocks_types):
        children_textnodes = text_to_textnodes(md_block)
        children = []
        for child in children_textnodes:
            children.append(child.text_node_to_html_node())
            
        match block_type:
            case BlockType.HEADING:
                heading_level = md_block.count("#")
                return f"<h{heading_level}>{children}</h{heading_level}>"
            case BlockType.CODE:
                return f"<code><pre>{children}</pre></code>"
            case BlockType.QUOTE:
                return f"<blockquote>{children}</blockquote>"
            case BlockType.UNORDERED_LIST:
                return f"<ul>{children}</ul>"
            case BlockType.ORDERED_LIST:
                return f"<ol>{children}</ol>"
            case BlockType.PARAGRAPH:
                return f"<p>{children}</p>"
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
            
            
