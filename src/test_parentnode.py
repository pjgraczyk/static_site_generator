import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
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
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
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

if __name__ == "__main__":
    unittest.main()
