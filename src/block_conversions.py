from enum import Enum
import re

# Convert a string of markdown to markdown blocks
def markdown_to_blocks(markdown):
    """
      This function takes a markdown file and breaks it up into blocks of code

      input: markdown md file.
      output: List of blocks
    """
    # Split blocks on whitespace
    blocks = markdown.split('\n\n')

    # remove whitespace
    blocks_no_wsp = [block.strip() for block in blocks]

    # remove empty blocks
    blocks_filled = [block for block in blocks_no_wsp if block]

    return blocks_filled
                            
# Create a class of markdown enums to classify blocks
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
              
def block_to_block_type(block:str) -> BlockType:
    #check blocktype with a bunch of if conditions to see which BlockType it is and return values

    # computations across types
    n_lines = len([line for line in block.split('\n') if line.strip()])
    
    # Headings
    if block.split('\n')[0].startswith("#") and len(re.findall("(?m)^[#]{1,6} ",block)) == 1:
        return BlockType.HEADING

    # code
    if re.search(r"^[\`]{3}.*[\`]{3}$", block, re.DOTALL):
        return BlockType.CODE

    # quotes (re.search() apparently only gives the first result, so use re.findall() instead)
    n_quotes = len(re.findall(r"(?m)^>", block))
    if n_quotes == n_lines:
        return BlockType.QUOTE

    # unordered list
    n_dashes = len(re.findall(r"(?m)^[-*+] ", block))
    if n_dashes == n_lines:
        return BlockType.UNORDERED_LIST

    # ordered list
    n_nos = len(re.findall(r"(?m)^(\d+)\. ", block))
    if n_nos == n_lines:
        # check the numbers are in order:
        i= 0
        j_list = list(re.findall(r"(?m)^(\d+)\. ", block))
        # If numbering doesn't begin at 1, return paragraph
        if int(j_list[0]) != 1:
            return BlockType.PARAGRAPH
        # If difference between consecutive numbers isn't 1, return paragraph
        for j in j_list:
            if int(j) - i != 1:
                # return error or Paragraph?
                print(f"entered paragraph loop at {j} and {i}")
                return BlockType.PARAGRAPH
            i = int(j)
            
        
        return BlockType.ORDERED_LIST

    # paragraph
    return BlockType.PARAGRAPH

