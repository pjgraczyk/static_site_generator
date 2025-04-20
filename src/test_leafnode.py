import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_value_and_tag(self):
        node = LeafNode("span", "Hello, Leaf!")
        self.assertEqual(node.to_html(), "<span>Hello, Leaf!</span>")

    def test_to_html_with_value_and_props(self):
        node = LeafNode("span", "Hello, Leaf!", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Hello, Leaf!</span>')

    def test_to_html_without_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("span", None)
            node.to_html()

    def test_to_html_without_tag(self):
        node = LeafNode(None, "Just a value")
        self.assertEqual(node.to_html(), "Just a value")

    def test_repr(self):
        node = LeafNode("span", "Hello, Leaf!", {"class": "highlight"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(span, Hello, Leaf!, children: None, {'class': 'highlight'})",
        )

    def test_to_html_with_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_anchor_and_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
