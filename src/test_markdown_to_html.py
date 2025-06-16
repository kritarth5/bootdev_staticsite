#imports
import unittest
from unittest.mock import patch, MagicMock
from markdown_to_html import markdown_to_html_node, extract_title
from block_conversions import block_to_block_type, markdown_to_blocks, BlockType
from textnode import TextNode, TextType
from htmlnode import LeafNode, HTMLNode, ParentNode

#tests
def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )




# test extract title
class TestExtractTitle(unittest.TestCase):
    
    def test_basic_title_extraction(self):
        """Test extracting a simple title"""
        markdown = "# Welcome to My Blog"
        result = extract_title(markdown)
        self.assertEqual(result, "Welcome to My Blog")
    
    def test_title_with_trailing_whitespace(self):
        """Test title with trailing spaces/tabs gets stripped"""
        markdown = "# My Title   \t  "
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")  # Should strip trailing whitespace
    
    def test_title_with_special_characters(self):
        """Test title containing special characters"""
        markdown = "# Title with $pecial Ch@rs & Numbers 123!"
        result = extract_title(markdown)
        self.assertEqual(result, "Title with $pecial Ch@rs & Numbers 123!")

    def test_empty_title(self):
        """Test header with no title text"""
        markdown = "# "
        result = extract_title(markdown)
        self.assertEqual(result, "")
    
    def test_title_with_leading_whitespace(self):
        """Test title with leading spaces/tabs gets stripped"""
        markdown = "#   \t  My Title"
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")  # Should strip leading whitespace
    
    def test_title_with_leading_and_trailing_whitespace(self):
        """Test title with both leading and trailing whitespace gets stripped"""
        markdown = "#   \t  My Title   \t  "
        result = extract_title(markdown)
        self.assertEqual(result, "My Title")  # Should strip both sides
    
    def test_no_header_raises_exception(self):
        """Test that missing header raises ValueError"""
        markdown = "This is just regular text"
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No Title Header Found")
    
    def test_empty_string_raises_exception(self):
        """Test that empty string raises ValueError"""
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_header_not_at_start_raises_exception(self):
        """Test that header not at beginning raises ValueError"""
        markdown = "Some text\n# My Title"
        with self.assertRaises(ValueError):
            extract_title(markdown)
       
