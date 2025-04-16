import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        if self.assertEqual(node, node2):
            print("Test passed, nodes are equal")

    def test_noteq(self):
        node = TextNode("Lorem ipsum", TextType.ITALIC, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        if self.assertNotEqual(node, node2):
            print("Test passed, nodes are not equal")

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        if self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)"):
            print("Test passed, repr is correct")

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        if self.assertEqual(node, node2):
            print("Test passed, nodes are equal")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        if self.assertEqual(
            repr(node), "TextNode(This is a text node, bold, https://www.google.com)"
        ):
            print("Test passed, repr is correct")

    def test_fail_second_arg(self):
        try:
            TextNode("This is a text node", "bold")
            self.assertRaises(TypeError)
        except TypeError:
            print("Test passed, second argument must be of type TextType")


if __name__ == "__main__":
    unittest.main()
