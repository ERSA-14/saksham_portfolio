import unittest

from textnode import TextNode, TextType , text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
        node = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertEqual(node, node)

        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertEqual(node1, node2)

        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Goodbye", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node1, node2)

        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hello", TextType.ITALIC, "https://example.com")
        self.assertNotEqual(node1, node2)

        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hello", TextType.BOLD, "https://google.com")
        self.assertNotEqual(node1, node2)

        node1 = TextNode("Hello", TextType.BOLD, None)
        node2 = TextNode("Hello", TextType.BOLD, None)
        self.assertEqual(node1, node2)

        node1 = TextNode("Hello", TextType.BOLD, None)
        node2 = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node1, node2)

        node = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node, "not a TextNode")

        node = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertEqual(repr(node), "TextNode(Hello, bold, https://example.com)") 
 
 
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node = TextNode("This is an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://i.imgur.com/zjjcJKZ.png", "alt": "This is an image"},
        )

        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

        node = TextNode("Click me!", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

        node = TextNode("Invalid", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

        

if __name__ == "__main__":
    unittest.main()
