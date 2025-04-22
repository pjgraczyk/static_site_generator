import unittest
from re import L

from node_utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestNodeUtils(unittest.TestCase):
    def test_split_nodes_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_different_delimiters(self):
        delimiters = [",", ";", ".", "/", "_"]
        for delimiter in delimiters:
            node = TextNode(f"This is text with a {delimiter} word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], delimiter, TextType.CODE)
            expected_nodes = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(" word", TextType.TEXT),
            ]
            self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_invalid_type(self):
        node = "This is not a TextNode"
        with self.assertRaises(TypeError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_split_nodes_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_multiple_nodes(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("Another text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("Another text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_no_delimiter(self):
        node = TextNode("This is text without a delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text without a delimiter", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_multiple_delimiters(self):
        node = TextNode(
            "This is text with a `code block` and another `code block`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_extraction_methods(self):
        text = "This is a [link](https://www.example.com) and this is a ![image](https://www.example.com/image.png)"
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertEqual(
            links,
            [
                ("link", "https://www.example.com"),
            ],
        )
        self.assertEqual(
            images,
            [
                ("image", "https://www.example.com/image.png"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
