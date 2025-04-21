import unittest

from node_utils import split_nodes_delimiter
from textnode import TextNode, TextType


class TestNodeUtils(unittest.TestCase):

    def test_split_nodes_delimiter_success(self):
        old_nodes = [TextNode("Hello,World", TextType.PARAGRAPH)]
        delimiter = ","
        text_type = TextType.PARAGRAPH
        expected_nodes = [
            TextNode("Hello", text_type),
            TextNode(delimiter, text_type),
            TextNode("World", text_type),
        ]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [TextNode("HelloWorld", TextType.PARAGRAPH)]
        delimiter = ","
        text_type = TextType.PARAGRAPH
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_delimiter_invalid_node_type(self):
        old_nodes = ["Hello,World"]  # Not a TextNode
        delimiter = ","
        text_type = TextType.PARAGRAPH
        with self.assertRaises(TypeError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_delimiter_empty_string(self):
        old_nodes = [TextNode("", TextType.PARAGRAPH)]
        delimiter = ","
        text_type = TextType.PARAGRAPH
        expected_nodes = [TextNode("", text_type)]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        old_nodes = [TextNode("Hello,,World", TextType.PARAGRAPH)]
        delimiter = ","
        text_type = TextType.PARAGRAPH
        expected_nodes = [
            TextNode("Hello", text_type),
            TextNode(delimiter, text_type),
            TextNode("", text_type),
            TextNode(delimiter, text_type),
            TextNode("World", text_type),
        ]
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_various_delimiters(self):
        delimiters = [";", ".", "\"", "'", "%", "`"]
        for delimiter in delimiters:
            old_nodes = [TextNode(f"Hello{delimiter}World{delimiter}!", TextType.PARAGRAPH)]
            text_type = TextType.PARAGRAPH
            expected_nodes = [
                TextNode("Hello", text_type),
                TextNode(delimiter, text_type),
                TextNode("World", text_type),
            ]
            result = split_nodes_delimiter(old_nodes, delimiter, text_type)
            self.assertEqual(result, expected_nodes)

if __name__ == "__main__":
    unittest.main()
