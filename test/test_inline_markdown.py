import unittest

from deepdiff import DeepDiff
from src.inline_markdown.inline_handlers import (
    extract_markdown_image,
    extract_markdown_link,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from src.inline_markdown.inline_parser import text_to_textnodes
from src.text_node import TextNode


class TextInlineMarkdown(unittest.TestCase):

    def assertTextNodeEqual(self, result_list, expected_list):
        diff = DeepDiff(result_list, expected_list, ignore_order=True)
        self.assertFalse(diff, f"Differences found: {diff}")

    def assertListEqualDeep(self, result_list, expected_list):
        diff = DeepDiff(result_list, expected_list, ignore_order=True)
        self.assertFalse(diff, f"Differences found: {diff}")

    def test_nested_delimiters(self):
        node = TextNode("This **is _nested_ bold** text", "text")
        nodes_list = [node]
        result = split_nodes_delimiter(nodes_list, "**")
        nested_node = TextNode("is _nested_ bold", "bold")
        expected = [TextNode("This ", "text"), nested_node, TextNode(" text", "text")]
        self.assertTextNodeEqual(result, expected)

    def test_text_without_delimiter(self):
        node = TextNode("Text without delimiter", "text")
        nodes_list = [node]
        result = split_nodes_delimiter(nodes_list, "**")
        expected = [TextNode("Text without delimiter", "text")]
        self.assertTextNodeEqual(result, expected)

    def test_invalid_text_type(self):
        node = TextNode("This is invalid type", "invalid")
        nodes_list = [node]
        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter(nodes_list, "*")
        self.assertTextNodeEqual(str(e.exception), "Invalid Text Type")

    def test_delimiter_near_string_limits(self):
        node = TextNode("***start and end***", "text")
        nodes_list = [node]
        result = split_nodes_delimiter(nodes_list, "*")
        expected = [
            TextNode("start and end", "italic"),
        ]
        self.assertTextNodeEqual(result, expected)

    def test_extract_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_image(text)
        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]
        self.assertTextNodeEqual(result, expected)

    def test_extract_link(self):
        text = "This is text with a [link](https://www.google.com) and [another](https://www.yahoo.com)"
        result = extract_markdown_link(text)
        expected = [
            ("link", "https://www.google.com"),
            ("another", "https://www.yahoo.com"),
        ]
        self.assertTextNodeEqual(result, expected)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
            "text",
        )
        nodes_list = [node]
        result = split_nodes_image(nodes_list)
        expected = [
            TextNode("This is an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
        ]
        self.assertTextNodeEqual(result, expected)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is a [link](https://www.google.com/new_page) and [another](https://www.yahoo.com)",
            "text",
        )
        result = split_nodes_link([node])
        expected = [
            TextNode("This is a ", "text"),
            TextNode("link", "link", "https://www.google.com/new_page"),
            TextNode(" and ", "text"),
            TextNode("another", "link", "https://www.yahoo.com"),
        ]
        self.assertTextNodeEqual(result, expected)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqualDeep(
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
