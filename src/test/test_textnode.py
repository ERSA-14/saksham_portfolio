import unittest

from markdown import markdown_to_blocks
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    text_node_to_html_node,
    text_to_textnodes,
)


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

        node = TextNode(
            "This is an image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
        )
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

        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node = TextNode("Text with `code1` and `code2` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node = TextNode("This has `no closing delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

        node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        node = TextNode("At the end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("At the end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

        node = TextNode("Text with `` empty", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode(" empty", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, matches)

        
        text = "This is plain text with no links or images."
        self.assertEqual([], extract_markdown_images(text))
        self.assertEqual([], extract_markdown_links(text))

        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        text = "This is plain text with no formatting."
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is plain text with no formatting.", TextType.TEXT)]
        self.assertEqual(nodes, expected)

        text = "**Bold** at the start and _italic_ after"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the start and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" after", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

        text = "Start with text and end with `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start with text and end with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)

        text = "![img1](url1) and ![img2](url2), [link1](url3), [link2](url4)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(", ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url3"),
            TextNode(", ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url4"),
        ]
        self.assertEqual(nodes, expected)

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

