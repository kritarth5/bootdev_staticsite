from ast import List
from htmlnode import HTMLNode, LeafNode
import htmlnode
from textnode import TextType, TextNode
import re


def text_node_to_html_node(text_node:TextNode) -> LeafNode:
    if text_node.text_type == TextType.NORMAL:
        if text_node.text:
            return LeafNode(tag=None, value=text_node.text, props=None)
        else:
            raise ValueError(f"No {text_node.text} found") 
    elif text_node.text_type == TextType.BOLD:
        if text_node.text:
            return LeafNode(tag="b",value=text_node.text, props=None)
        else:
            raise ValueError(f"No {text_node.text} found") 
    elif text_node.text_type == TextType.ITALIC:
        if text_node.text:
            return LeafNode(tag="i",value=text_node.text, props=None)
        else:
            raise ValueError(f"No {text_node.text} found") 
    elif text_node.text_type == TextType.CODE:
        if text_node.text:
            return LeafNode(tag="code",value=text_node.text, props=None)
        else:
            raise ValueError(f"No {text_node.text} found") 
    elif text_node.text_type == TextType.LINK:
        if text_node.text and text_node.url:
            return LeafNode(tag="a",value=text_node.text, props={"href":text_node.url})
        else:
            raise ValueError(f"Either of text_node's text({text_node.text}) or url({text_node.url}) missing")
    elif text_node.text_type == TextType.IMAGE:
        if text_node.text and text_node.url:
            return LeafNode(tag="img",value="", props={"src":text_node.url, "alt":text_node.text})
        else:
            raise ValueError(f"Either of text_node's text({text_node.text}) or url({text_node.url}) missing")
    else:
        raise TypeError(f"Invalid Text type: {text_node.text_type} passed!")
    


def split_nodes_delimiter(old_nodes:List, delimiter:str, text_type:TextType) -> List:
    # initialise new nodes variable
    new_nodes = []
    # loop over old_nodes
    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            split_nodes = node.text.split(delimiter)
            # if total length is odd then there's an unbalanced delimiter. make cases and confirm this is the case.
            if len(split_nodes) % 2 == 0:
                raise ValueError(f"Unmatched delimter {delimiter} found. Check input nodes")
            for i in range(len(split_nodes)):
                # check if node is non-empty
                if split_nodes[i]:
                    # even nodes become text (0, 2, 4)
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_nodes[i], TextType.NORMAL))
                    # odd nodes become text_type (1,3,5) etc.
                    else:
                        new_nodes.append(TextNode(split_nodes[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes

            
def extract_markdown_images(text):
    #get a list of all urls and alt text from the string using regex
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    #return matches
    return matches

def extract_markdown_links(text):

    #get a list of all urls and alt text from the string using regex
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    #return matches
    return matches

def split_nodes_image(old_nodes:List) -> List:
    # New nodelist initialise. This is what we return at the end of the code
    new_nodes = []
    
    # loop over every  we will need to be able to split raw markdown text into TextNodes based on images and links.
    for node in old_nodes:
        # If this isn't a text node, skip
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        # if the node has no images, return the same text string back
        matches = list(re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",node.text))
        if not matches:
            new_nodes.append(TextNode(node.text, TextType.NORMAL))
            continue
        
        # initialise a last_end variable which starts at 0 and moves to the end of the match
        last_end = 0
        
        # every node is a text_node to be split out of with images and links
        for match in re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",node.text):
            # save the first length of string before match as a text (from last_end, which is 0 at the beginning)
            # check if it exists first, ex, link is at the beginning or it's the second of two consecutive links.
            if node.text[last_end:match.start()]:
                new_nodes.append(TextNode(node.text[last_end:match.start()], TextType.NORMAL))
            
            # i should check matches have what we expect, but for now, expect match_1 is alt_text, and match_2 is image_link
            if match.group(1) and match.group(2):
                new_nodes.append(TextNode(match.group(1), TextType.IMAGE, url=match.group(2)))

            # If empty alt text or url, save it as a text node
            else:
                new_nodes.append(TextNode(text.node[match.start(): match.end()], TextType.NORMAL))

            last_end = match.end()             
            # There should be one other text node after this. Save it outside the loop.

                
        # save last bit of string
        if node.text[last_end:]:
            new_nodes.append(TextNode(node.text[last_end:], TextType.NORMAL))
            continue

    # return list of nodes            
    return new_nodes

def split_nodes_link(old_nodes:List) -> List:
    # New nodelist initialise. This is what we return at the end of the code
    new_nodes = []
    
    # loop over every  we will need to be able to split raw markdown text into TextNodes based on links and links.
    for node in old_nodes:
        # If node isn't a text type go to the next one:
        # If this isn't a text node, skip
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        # if the node has no links, return the same text string back
        matches = list(re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",node.text))
        if not matches:
            new_nodes.append(TextNode(node.text, TextType.NORMAL))
            continue

        # initialise a last_end variable which starts at 0 and moves to the end of the match
        last_end = 0
        
        # every node is a text_node to be split out of with links and links
        for match in re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",node.text):

            # save the first length of string before match as a text (from last_end, which is 0 at the beginning)
            # check if it exists first, ex, link is at the beginning or it's the second of two consecutive links.
            if node.text[last_end:match.start()]:
                new_nodes.append(TextNode(node.text[last_end:match.start()], TextType.NORMAL))
            
            # i should check matches have what we expect, but for now, expect match_1 is alt_text, and match_2 is link_link
            # Check if link text link is non-empty, if any are empty, store as text
            if match.group(1) and match.group(2):
                new_nodes.append(TextNode(match.group(1), TextType.LINK, url=match.group(2)))

            else:
                new_nodes.append(TextNode(node.text[match.start():match.end()], TextType.NORMAL))

            last_end = match.end()             
            # There should be one other text node after this. Save it outside the loop.
                
        # save last bit of string
        if node.text[last_end:]:
            new_nodes.append(TextNode(node.text[last_end:], TextType.NORMAL))

        
    # return list of nodes            
    return new_nodes


def text_to_textnodes(text):
    """
    From a string of text, extract the code, italic, bold, image and link portions

    input: a string of text

    output: a list of split nodes
    """

    old_nodes = [TextNode(text, TextType.NORMAL)]
    # Split regular texty parts by delimiter first
    nodes_part_1 = split_nodes_link(old_nodes)
    nodes_part_2 = split_nodes_image(nodes_part_1)
    nodes_part_3 = split_nodes_delimiter(nodes_part_2,"`",text_type=TextType.CODE)
    nodes_part_4 = split_nodes_delimiter(nodes_part_3,"**",text_type=TextType.BOLD)
    nodes_part_5 = split_nodes_delimiter(nodes_part_4,"_",text_type=TextType.ITALIC)

    return nodes_part_5
