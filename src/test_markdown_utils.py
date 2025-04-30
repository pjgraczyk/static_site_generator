import unittest

from markdown_utils import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)


def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )


def test_markdown_to_blocks_empty(self):
    md = ""
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, [])
    
def test_markdown_to_blocks_no_newline(self):
    md = "This is a single paragraph without newlines."
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a single paragraph without newlines."])
    
def test_markdown_to_blocks_multiple_newlines(self):
    md = "This is a paragraph.\n\n\nThis is another paragraph."
    blocks = markdown_to_blocks(md)
    self.assertEqual(blocks, ["This is a paragraph.", "This is another paragraph."])
    
def test_block_to_block_type(self):
    md = """
# Heading 1
This is a code block

```
def hello_world():
    print("Hello, world!")
```

> This is a quote
- Item 1
- Item 2
1. First item
2. Second item
"""
    blocks = markdown_to_blocks(md)
    block_types = [
        block_to_block_type(block) for block in blocks
    ]
    expected_types = [
        (BlockType.HEADING, 1),
        (BlockType.PARAGRAPH, None),
        (BlockType.CODE, None),
        (BlockType.QUOTE, None),
        (BlockType.UNORDERED_LIST, None),
        (BlockType.ORDERED_LIST, None),
    ]
    self.assertEqual(block_types, expected_types)

if __name__ == "__main__":
    unittest.main()
