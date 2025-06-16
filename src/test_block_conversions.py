#imports
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from re import NOFLAG, findall
from block_conversions import markdown_to_blocks, block_to_block_type, BlockType


# tests

class TestBlocksToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md ="""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

              
"""
              
        blocks = markdown_to_blocks(md)
#        print(blocks)
#        print(len(blocks))
#        print(">>>>>>>>>>>>>>>>>>")
        self.assertEqual(
        blocks,
        [
         "This is **bolded** paragraph",
         
         "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
         
         "- This is a list\n- with items",
        ],
        )


class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_single_hash(self):
        """Test single # heading"""
        result = block_to_block_type("# This is a heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_multiple_hashes(self):
        """Test headings with 2-6 hashes"""
        test_cases = [
            "## Level 2 heading",
            "### Level 3 heading", 
            "#### Level 4 heading",
            "##### Level 5 heading",
            "###### Level 6 heading"
        ]
        for heading in test_cases:
            with self.subTest(heading=heading):
                result = block_to_block_type(heading)
                self.assertEqual(result, BlockType.HEADING)
    
                
