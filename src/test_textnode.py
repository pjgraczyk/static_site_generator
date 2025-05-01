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
        if self.assertEqual(
            repr(node), 'TextNode("This is a text node", TextType.BOLD, "None")'
        ):
            print("Test passed, repr is correct")

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        if self.assertEqual(node, node2):
            print("Test passed, nodes are equal")

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        if self.assertEqual(
            repr(node),
            'TextNode("This is a text node", TextType.BOLD, "https://www.google.com")',
        ):
            print("Test passed, repr is correct")

    def test_fail_second_arg(self):
        try:
            TextNode("This is a text node", "bold")
            self.assertRaises(TypeError)
        except TypeError:
            print("Test passed, second argument must be of type TextType")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(
            "This is a text node",
            TextType.IMAGE,
            url="https://www.google.com",
            alt="This is a text node",
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.google.com", "alt": "This is a text node"},
        )


if __name__ == "__main__":
    unittest.main()
