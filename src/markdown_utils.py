import re

from enum import Enum


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
    blocks = [block.strip() for block in blocks if block.strip()]
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
