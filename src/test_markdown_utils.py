import unittest

from markdown_utils import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    BlockType,
)


class TestMarkdownUtils(unittest.TestCase):
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
        block_types = [block_to_block_type(block) for block in blocks]
        expected_types = [
            (BlockType.HEADING),
            (BlockType.PARAGRAPH),
            (BlockType.CODE),
            (BlockType.QUOTE),
            (BlockType.UNORDERED_LIST),
            (BlockType.ORDERED_LIST),
        ]
        self.assertEqual(block_types, expected_types)

    def test_block_to_block_type_empty(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, (BlockType.PARAGRAPH))

    def test_block_to_block_type_code(self):
        block = "```\ncode\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, (BlockType.CODE))

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, (BlockType.QUOTE))

    def test_block_to_block_type_unordered_list(self):
        block = "- Item 1\n\n- Item 2"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, (BlockType.UNORDERED_LIST))

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with a new line
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith a new line</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
- Item 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_image(self):
        md = """
![alt text](https://example.com/image.png) Hello
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><img alt="alt text" src="https://example.com/image.png"></img> Hello</p></div>',
        )

    def test_link(self):
        md = """
[Link text](https://example.com)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><a href="https://example.com">Link text</a></p></div>',
        )

    def test_bold(self):
        md = """This excerpt is **This is bold text** and this one is not"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This excerpt is <b>This is bold text</b> and this one is not</p></div>",
        )

    def test_italic(self):
        md = """
_This is italic text_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p><i>This is italic text</i></p></div>",
        )

    def test_heading_levels(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        # TODO: Headings are recognised only with double newlines like above
        # TODO: should they be recognised with single newlines too?
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )


if __name__ == "__main__":
    unittest.main()
