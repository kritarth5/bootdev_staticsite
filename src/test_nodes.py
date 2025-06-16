# Imports to file
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from re import NOFLAG, findall

# test file to test textnodes and HTML Nodes

# Test TextNode Function
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
# Test HTML Nodes functions
class TestHTMLNode(unittest.TestCase):
    def test_tags(self):
        html1 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        html2 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        self.assertEqual(html1.tag,html2.tag)

    def test_value(self):
        html1 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        html2 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        self.assertEqual(html1.value,html2.value)

    def test_children(self):
        html1 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        html2 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        self.assertEqual(html1.children,html2.children)

    def test_props(self):
        html1 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        html2 = HTMLNode("div", 10, ["I"], props={"h":"hello"})
        self.assertEqual(html1.props,html2.props)

# Test LeafNode prints what's expected
class TestLeafNode(unittest.TestCase):
    def test_value(self):
        leaf = LeafNode(value="this is just text")
        self.assertEqual(leaf.value, "this is just text")

    def test_valuetag(self):
        leaf2 = LeafNode("p", "this is just text")
        self.assertEqual(leaf2.to_html(), "<p>this is just text</p>")


    def test_valuetagprop(self):
        leaf2 = LeafNode( "a","hello_world", props={"href":"https://google.com"})
        self.assertEqual(leaf2.to_html(), '<a href="https://google.com" >hello_world</a>')


# Test Parent Node
class TestParentNode(unittest.TestCase):
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
            "<div><span><b>grandchild</b></span></div>",)

        
        
        
    

