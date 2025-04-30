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
    match block:
        case block if block.startswith("#"):
            match block:
                case block if block.startswith("######"):
                    return BlockType.HEADING, 6
                case block if block.startswith("#####"):
                    return BlockType.HEADING, 5
                case block if block.startswith("####"):
                    return BlockType.HEADING, 4
                case block if block.startswith("###"):
                    return BlockType.HEADING, 3
                case block if block.startswith("##"):
                    return BlockType.HEADING, 2
                case block if block.startswith("#"):
                    return BlockType.HEADING, 1
            return BlockType.HEADING, 1
        case block if block.startswith("```") and block.endswith("```"):
            return BlockType.CODE, None
        case block if all(line.startswith(">") for line in block.split("\n") if line):
            return BlockType.QUOTE, None
        case block if all(line.startswith("- ") for line in block.split("\n") if line):
            return BlockType.UNORDERED_LIST, None
        case block if all(re.match(r"^\d+\.", line) for line in block.split("\n") if line):
            return BlockType.ORDERED_LIST, None
        case _:
            return BlockType.PARAGRAPH, None
