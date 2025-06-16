# This file converts a string/page of markdown to an HTMLNode

#imports
from os.path import isfile
from textnode import TextType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_conversions import text_node_to_html_node, text_to_textnodes, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from block_conversions import BlockType, markdown_to_blocks, block_to_block_type
from typing import List
import re
import os

# functions
def markdown_to_html_node(markdown:str) -> ParentNode:
    # Break up markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # initilaise a child_nodes list that stores all ParentNodes that come out of the for loop below
    child_nodes = []

    for block in blocks:
        # check what kind of a block it is and convert it to the appropriate ParentNode
        # headings
        if block_to_block_type(block) == BlockType.HEADING:

            # extract how many "#"'s there are to determine which heading this is.
            match = re.match(r'^([#]{1,6}) (.*)', block)
            if match:
                nh = len(match.group(1))
                heading_text = match.group(2)
            
                # create HTMLNode with these characteristics
                node = LeafNode(tag=f"h{nh}", value=heading_text, props=None)

                # add to list of children nodes
                child_nodes.append(node)
            else:
                raise ValueError(f"Invalid Heading {block}")

        # code to ParentNode
        elif block_to_block_type(block) == BlockType.CODE:
            # extract code text
            match = re.match(r"^```(.*)```$",block, re.DOTALL)
            if match:
                
                code_text = match.group(1)

                # Create text node of code
                code_node = TextNode(code_text, TextType.CODE)

                # convert text node to html node
                code_node = text_node_to_html_node(code_node)

                # add a pre tag by converting it to a HTML Node
                pre_code_node = ParentNode(tag="pre", children=[code_node])
                child_nodes.append(pre_code_node)

            else:
                raise ValueError(f"Invalid code block {block}")
                                 

        # ordered list to ParentNode
        elif block_to_block_type(block) == BlockType.ORDERED_LIST:
            # Make a list of ParentNodes of list items
            HTML_List = []
            # Extract all items into a list of their own
            list_items = re.findall(r'(?m)^\d+\. (.*)$' , block)

            # loop over each line of the list and convert it to a list of html nodes
            for list_item in list_items:
                children_nodes = text_to_children(list_item)
                list_node = ParentNode(tag="li", children=children_nodes)
                HTML_List.append(list_node)

            # wrap the HTML_List of children nodes in an "ol" tag
            Ordered_HTML = ParentNode(tag="ol", children=HTML_List)
            child_nodes.append(Ordered_HTML)

        # unordered list to ParentNode
        elif block_to_block_type(block) == BlockType.UNORDERED_LIST:
            # Make a list of ParentNodes of list items
            HTML_List = []
            # Extract all items into a list of their own
            list_items = re.findall(r'(?m)^[-*+] (.*)$' , block)

            # loop over each line of the list and convert it to a list of html nodes
            for list_item in list_items:
                children_nodes = text_to_children(list_item)
                list_node = ParentNode(tag="li", children=children_nodes)
                HTML_List.append(list_node)

            # wrap the HTML_List of children nodes in an "ul" tag
            Unordered_HTML = ParentNode(tag="ul", children=HTML_List)
            child_nodes.append(Unordered_HTML)

        # paragraph to ParentNode
        elif block_to_block_type(block) == BlockType.PARAGRAPH:
            # Make a list of ParentNodes of list items
            HTML_List = text_to_children(block)

            # wrap the HTML_List of children nodes in an "p" tag
            Paragraph_HTML = ParentNode(tag="p", children=HTML_List)
            child_nodes.append(Paragraph_HTML)


        # blockquote to ParentNode
        elif block_to_block_type(block) == BlockType.QUOTE:
            # remove all > from lines of the block quotes
            block = re.sub(r'(?m)^>', '', block).strip()
            # Make a list of nodes to hold all inline elements
            HTML_quote = ParentNode(tag="blockquote", children=text_to_children(block))
            
            child_nodes.append(HTML_quote)

        else:
            raise ValueError(f"Unknown BlockType Found in {block}")

    # Return the final HTML Node with a div around the functions
    return ParentNode(tag="div", children=child_nodes)

def text_to_children(text:str) -> List:
    """
      Function that converts text to all inline object possible as HTMLNodes
    """
    # Convert inline text to textnodes
    textnodes = text_to_textnodes(text)

    # convert textnodes list to an HTMLNodes list
    htmlnodes = []

    for node in textnodes:
        htmlnode = text_node_to_html_node(node)
        htmlnodes.append(htmlnode)

    return htmlnodes
    
    
def extract_title(markdown):
    match = re.search(r'^# (.*)', markdown)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("No Title Header Found")
                          
def generate_page(from_path, template_path, dest_path, basepath):
    """ Generate one html page from a markdown to html"""
    # Print which page is being generated
    print(f"generating page from {from_path} to destination {dest_path} using a template {template_path}")

    # read in the markdown file from the from_path
    with open(from_path, 'r') as file:
        markdown_page = file.read()

    # read in template file and save it
    with open(template_path, 'r') as file:
        template_page = file.read()

    # convert markdown to html string
    html_string = markdown_to_html_node(markdown_page).to_html()

    # Ge title of the markdown page
    title_string = extract_title(markdown_page)
    
    # replace the placeholders in the template_page string with the title and body we've extracted.
    template_page = template_page.replace("{{ Title }}", title_string)
    template_page = template_page.replace("{{ Content }}", html_string)
    template_page = template_page.replace('href="/', f'href="{basepath}')
    template_page = template_page.replace('src="/', f'src="{basepath}')
    
    # write the string to destination path
    dest_directory_path = os.path.dirname(dest_path)

    # make directories if they don't exist before writing the file
    if not os.path.exists(dest_directory_path) and dest_directory_path:
        os.makedirs(dest_directory_path, exist_ok=True)

    # write the file to dest_path
    with open(dest_path, 'w') as file:
        file.write(template_page)
            
        
def generate_page_recursively(from_path, template_path, dest_path, basepath):
    """ Copy /content contents into /public for website recursively"""
    # Print what's happening:
    # TODO: Make the print output nicer. 
    print(f"Recursively copy {from_path} to {dest_path}")

    # get all files in current directory
    files_list = os.listdir(from_path)

    # loop over files/directories in files_list:
    for file in files_list:
        # update source and destination paths
        new_source_path = os.path.join(from_path, file)
        new_dest_path = os.path.join(dest_path, file)
        
        # if the file is a markdown file
        if os.path.isfile(new_source_path) and is_markdown(new_source_path):
            # make an html file of the markdown file
            new_dest_path = re.sub(r'.md$',".html", new_dest_path)

            # ensure all directories to the file exist:
            os.makedirs(os.path.dirname(new_dest_path), exist_ok=True)

            # generate html from markdown
            generate_page(new_source_path, template_path, new_dest_path, basepath)
                

        # If filepath is actually a directory, recurse:
        elif os.path.isdir(new_source_path):

            # make directories
            os.makedirs(new_dest_path, exist_ok=True)

            # recurse and call the function again:
            generate_page_recursively(new_source_path, template_path, new_dest_path, basepath)

        # if file exists but it isn't a markdown file, continue
        else:
            continue
         
            


def is_markdown(filepath):
    """ Check if file ends with markdown extensions"""
    return filepath.lower().endswith(('.md', '.markdown','.mkd'))



        
