import unittest

from text_node import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_not_textnode(self):
        node1 = TextNode("This is a text node", "italic")
        result = node1.__eq__("non TextNode")
        self.assertIs(result, NotImplemented)


if __name__ == "__main__":
    unittest.main()
