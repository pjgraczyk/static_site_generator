import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr_html_node(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_html = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            props={"href": "https://www.google.com"},
        )
        expected_html = '<a href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_edge_cases(self):
        # Test with no children
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

        # Test with multiple children
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2"),
                LeafNode("li", "Item 3"),
            ],
        )
        expected_html = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        self.assertEqual(node.to_html(), expected_html)

        # Test with nested ParentNode objects
        child_node = ParentNode(
            "span",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "Italic"),
            ],
        )
        parent_node = ParentNode("div", [child_node])
        expected_html = "<div><span><b>Bold</b> and <i>Italic</i></span></div>"
        self.assertEqual(parent_node.to_html(), expected_html)

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

    def test_repr_leaf_node(self):
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
