# import libraries
import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from inline_conversions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from re import NOFLAG, findall

# Tests for inline conversion to HTMLnode by delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    """ Tests for inline text delimited converters"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create sample nodes for testing
        self.normal_node = TextNode("This is normal text", TextType.NORMAL)
        self.bold_node = TextNode("This is bold text", TextType.BOLD)
        self.italic_node = TextNode("This is italic text", TextType.ITALIC)
    
    def test_single_delimiter_pair(self):
        """Test splitting with a single pair of delimiters"""
        nodes = [TextNode("This is `code` text", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL)
        ]
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
    
    def test_multiple_delimiter_pairs(self):
        """Test splitting with multiple pairs of delimiters"""
        nodes = [TextNode("Start `code1` middle `code2` end", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code1")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        self.assertEqual(result[3].text, "code2")
        self.assertEqual(result[3].text_type, TextType.CODE)
        self.assertEqual(result[4].text, " end")
        self.assertEqual(result[4].text_type, TextType.NORMAL)
    
    def test_no_delimiters(self):
        """Test with text that has no delimiters"""
        nodes = [TextNode("This has no special formatting", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This has no special formatting")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
                
    def test_empty_string_handling(self):
        """Test handling of empty strings after splitting"""
        nodes = [TextNode("Start``end", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # Should only get "Start" and "end" since empty strings are filtered out
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "Start")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "end")
        self.assertEqual(result[1].text_type, TextType.NORMAL)
    
    def test_delimiter_at_start(self):
        """Test delimiter at the beginning of text"""
        nodes = [TextNode("`code` at start", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "code")
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, " at start")
        self.assertEqual(result[1].text_type, TextType.NORMAL)
    
    def test_delimiter_at_end(self):
        """Test delimiter at the end of text"""
        nodes = [TextNode("At end `code`", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "At end ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
    
    def test_only_delimited_text(self):
        """Test text that is entirely delimited"""
        nodes = [TextNode("`entirelycode`", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "entirelycode")
        self.assertEqual(result[0].text_type, TextType.CODE)
    
    def test_non_normal_nodes_unchanged(self):
        """Test that non-NORMAL nodes pass through unchanged"""
        nodes = [
            TextNode("Normal `code` text", TextType.NORMAL),
            TextNode("Bold text with `backticks`", TextType.BOLD),
            TextNode("Italic text with `backticks`", TextType.ITALIC)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # First node should be split into 3 parts
        self.assertEqual(result[0].text, "Normal ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)
        
        # Second and third nodes should be unchanged
        self.assertEqual(result[3].text, "Bold text with `backticks`")
        self.assertEqual(result[3].text_type, TextType.BOLD)
        self.assertEqual(result[4].text, "Italic text with `backticks`")
        self.assertEqual(result[4].text_type, TextType.ITALIC)
    
    
    def test_different_delimiters(self):
        """Test with different delimiter characters"""
        # Test asterisk delimiter
        nodes = [TextNode("This is *italic* text", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text, "italic")
        self.assertEqual(result[1].text_type, TextType.ITALIC)
        self.assertEqual(result[2].text, " text")
        
        # Test double asterisk delimiter
        nodes = [TextNode("This is **bold** text", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
    
    def test_empty_list(self):
        """Test with empty list of nodes"""
        result = split_nodes_delimiter([], "`", TextType.CODE)
        self.assertEqual(result, [])
    
    def test_multiple_unmatched_delimiters(self):
        """Test multiple unmatched delimiters"""
        nodes = [TextNode("Too `many `delimiters `here", TextType.NORMAL)]
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    def test_single_delimiter_at_end(self):
        """Test single delimiter at end raises error"""
        nodes = [TextNode("Text with trailing `", TextType.NORMAL)]
        
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    def test_whitespace_only_between_delimiters(self):
        """Test whitespace-only content between delimiters"""
        nodes = [TextNode("Start ` ` end", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        # Should include the space as valid content
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, " ")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, " end")
    
    def test_consecutive_delimiters_multiple_pairs(self):
        """Test multiple consecutive delimiter pairs"""
        nodes = [TextNode("Text `code1``code2` more", TextType.NORMAL)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].text, "Text ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "code1")
        self.assertEqual(result[1].text_type, TextType.CODE)
        self.assertEqual(result[2].text, "code2")
        self.assertEqual(result[2].text_type, TextType.CODE)
        self.assertEqual(result[3].text, " more")
        self.assertEqual(result[3].text_type, TextType.NORMAL)


class TestMarkdownImageExtractor(unittest.TestCase):
    
    def test_basic_image(self):
        """Test basic markdown image syntax"""
        text = "![alt text](https://example.com/image.jpg)"
        expected = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_empty_alt_text(self):
        """Test image with empty alt text"""
        text = "![](https://example.com/image.jpg)"
        expected = [("", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
        
    def test_multiple_images(self):
        """Test multiple images in one string"""
        text = "![first](url1) and ![second](url2)"
        expected = [("first", "url1"), ("second", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitNodesImage(unittest.TestCase):
    """Comprehensive unit tests for split_nodes_link function"""

    # Basic functionality tests
    def test_plain_text_no_html(self):
        """Test plain text with no HTML tags"""
        html = TextNode("Just plain text", TextType.NORMAL)
        expected = [TextNode("Just plain text", TextType.NORMAL)]
        result = split_nodes_image([html])
        self.assertEqual(result, expected)

    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
         TextNode("This is text with an ", TextType.NORMAL),
         TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
         TextNode(" and another ", TextType.NORMAL),
         TextNode(
             "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
         ),
            ],
            new_nodes,
        )

class TestSplitNodesLink(unittest.TestCase):
    """Comprehensive unit tests for split_nodes_link function"""

    # Basic functionality tests
    def test_plain_text_no_html(self):
        """Test plain text with no HTML tags"""
        html = TextNode("Just plain text", TextType.NORMAL)
        expected = [TextNode("Just plain text", TextType.NORMAL)]
        result = split_nodes_link([html])
        self.assertEqual(result, expected)

    # Only html, no text
    def test_html_no_normal_text(self):
        """Test plain text with no HTML tags"""
        html = TextNode("[Linka Texta](www.nothing.com)", TextType.NORMAL)
        expected = [TextNode("Linka Texta", TextType.LINK, url="www.nothing.com")]
        result = split_nodes_link([html])
        self.assertEqual(result, expected)
        
    # test two links in the html
    def test_two_links(self):
        node = TextNode(
            "This is text with an [Link Text](https://i.imgur.com/zjjcJKZ.png) and another [Linka Texta](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
         TextNode("This is text with an ", TextType.NORMAL),
         TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
         TextNode(" and another ", TextType.NORMAL),
         TextNode(
             "Linka Texta", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
         ),
            ],
            new_nodes,
        )

    # Test three links in the same html string
    def test_three_links(self):
        node = TextNode(
            "This is text with an [Link Text](https://i.imgur.com/zjjcJKZ.png) and another [Linka Texta](https://i.imgur.com/3elNhQu.png)[Linka Texta](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
         TextNode("This is text with an ", TextType.NORMAL),
         TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
         TextNode(" and another ", TextType.NORMAL),
         TextNode("Linka Texta", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
         TextNode("Linka Texta", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
         ],
            new_nodes,
        )

    # Test consecutive links (2) without any spaces or text between them        
    def test_consecutive_links(self):
        node = TextNode(
            "This is text with an [Link Text](https://i.imgur.com/zjjcJKZ.png) [Linka Texta](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
         TextNode("This is text with an ", TextType.NORMAL),
         TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
         TextNode(" ", TextType.NORMAL),
         TextNode("Linka Texta", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )

    # Test if link is at the beginning of the string
    def test_start_link(self):
        node = TextNode(
            "[Link Text](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    # Test if link is at the end of the markdown string        
    def test_end_link(self):
        node = TextNode(
            "The link is at the end [Link Text](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [TextNode("The link is at the end ", TextType.NORMAL),TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    # Test if there are nospaces between links        
    def test_nospace_links(self):
        node = TextNode(
            "The link is at the end [Link Text](https://i.imgur.com/zjjcJKZ.png)[Link Text](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [TextNode("The link is at the end ", TextType.NORMAL),
         TextNode("Link Text",TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
         TextNode("Link Text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],
        new_nodes,
        )

    # This fails for whatever reason. Need to re-examine regex here. 
    def test_malformed_link_text(self):
        """Check for malformed link text"""
        html = TextNode("[Linka [Texta]](www.nothing.com)", TextType.NORMAL)
        expected = [TextNode("[Linka [Texta]](www.nothing.com)", TextType.NORMAL)]
        result = split_nodes_link([html])
        self.assertEqual(result, expected)

    def test_malformed_urls(self):
        """Test for malformed urls"""
        html = TextNode("[Linka Texta](www.nothing().com)", TextType.NORMAL)
        expected = [TextNode("[Linka Texta](www.nothing().com)", TextType.NORMAL)]
        result = split_nodes_link([html])
        self.assertEqual(result, expected)

    def test_missing_link_text(self):
        """Test for missing link text"""
        html = TextNode("[](www.nothing().com)", TextType.NORMAL)
        expected = [TextNode("[](www.nothing().com)", TextType.NORMAL)]
        result = split_nodes_link([html])
        self.assertEqual(result, expected)
        
    def test_missing_urls(self):
        """Test for missing urls"""
        html = TextNode("[Link Text]()", TextType.NORMAL)
        expected = [TextNode("[Link Text]()", TextType.NORMAL)]
        result = split_nodes_link([html])
        self.assertEqual(result, expected)

class TestHTMLToNodes(unittest.TestCase):
    """Comprehensive tests for HTML to nodes converter"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.maxDiff = None

    def test_one_of_each(self):
        """ Test one of each type of delimiter, image and link and see if it's parsed correctly"""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = text_to_textnodes(text)
        result = [
        TextNode("This is ", TextType.NORMAL),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.NORMAL),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.NORMAL),
        TextNode("link", TextType.LINK, "https://boot.dev"),
        ]


#        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<----------------------------------------")
#        print(part_1)
#
#        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<----------------------------------------")
#        print(part_2)
#        print("---------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        self.assertEqual(result, expected)
        
# TextNode to Leafnode converstion texts
class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")        
       
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")        

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")        

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")        

    def test_link(self):
        node = TextNode("This is a url node", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a url node")
        self.assertEqual(html_node.props["href"], "https://google.com")

    def test_broken_link(self):
        node = TextNode("This is a url node", TextType.LINK)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_broken_text(self):
        node = TextNode("", TextType.LINK)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_image(self):
        """Test image with alt text and URL creates proper img tag"""
        node = TextNode("A beautiful sunset", TextType.IMAGE, "sunset.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Images have empty value
        self.assertEqual(html_node.props["src"], "sunset.jpg")
        self.assertEqual(html_node.props["alt"], "A beautiful sunset")

    def test_image_missing_url(self):
        """Test image with missing URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE)  # No URL provided
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("url", str(context.exception).lower())

    def test_image_empty_url(self):
        """Test image with empty URL raises ValueError"""
        node = TextNode("Alt text", TextType.IMAGE, "")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("url", str(context.exception).lower())


    def test_image_missing_alt_text(self):
        """Test image with missing alt text raises ValueError"""
        node = TextNode("", TextType.IMAGE, "image.jpg")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("text", str(context.exception).lower())

    def test_image_none_alt_text(self):
        """Test image with None alt text raises ValueError"""
        node = TextNode(None, TextType.IMAGE, "image.jpg")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_missing_both(self):
        """Test image with missing alt text and URL raises ValueError"""
        node = TextNode("", TextType.IMAGE, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

