import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestMyClass(unittest.TestCase):
    def test_some_method(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

        node = HTMLNode(tag="p", value="Hello, world!", props={"class": "greeting"})
        self.assertEqual(
            repr(node), "HTMLNode(p, Hello, world!, None, {'class': 'greeting'})"
        )

        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

        node = LeafNode("p", "Hello, world!", {"class": "greeting"})
        self.assertEqual(
            repr(node), "LeafNode(p, Hello, world!, {'class': 'greeting'})"
        )

        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

        node = ParentNode("div", [LeafNode("p", "text")], {"class": "container"})
        self.assertEqual(
            repr(node),
            "ParentNode(div, [LeafNode(p, text, None)], {'class': 'container'})",
        )


if __name__ == "__main__":
    unittest.main()
