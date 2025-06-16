import os
import shutil
from markdown_to_html import generate_page, generate_page_recursively,is_markdown
import sys

def main():
    # grab arguments for github pages build:
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    # define paths
    # There should be someway to pass these variables to main as well. 
    public_path = "/Users/kjha/code/bootdev/bootdev_staticsite/docs"
    static_path = "/Users/kjha/code/bootdev/bootdev_staticsite/static"
    
    # call function to copy and paste from source to destination
    copy_source_destination(static_path, public_path)

    # generate a page as an example
    from_page = "/Users/kjha/code/bootdev/bootdev_staticsite/content"
    template_page = "/Users/kjha/code/bootdev/bootdev_staticsite/template.html"
    destination_page = "/Users/kjha/code/bootdev/bootdev_staticsite/docs"

    generate_page_recursively(from_page, template_page, destination_page, basepath)

def copy_source_destination(static_path:str, public_path:str) -> None:

    # Function to delete contents of public
    if os.path.isdir(public_path):
        shutil.rmtree(public_path)
    os.mkdir(public_path)

    # Function to recursively copy contents of static to public
    recurse_copy_source_destination(static_path,static_path, public_path)

def recurse_copy_source_destination(pwd:str,static_path:str, public_path:str):
    # List files in pwd.
    files_list = os.listdir(pwd)

    # Define relative path
    rel_path = os.path.relpath(pwd, static_path)

    # take care of corner case when rel_path is .
    if rel_path == ".":
        rel_path = ""
        
    # loop over files in file_list
    for file in files_list:

        # get source path
        source_path = os.path.join(pwd, file)

        # define copy path
        if rel_path:
            copy_path = os.path.join(public_path, rel_path, file)
        else:
            copy_path = os.path.join(public_path, file)

        # if we hit upon a file, we copy it.
        # Assume all directories here are already made, deal with them when we hit a directory
        if os.path.exists(source_path) and os.path.isfile(source_path):

            # copy files from pwd
            shutil.copy(source_path, copy_path)
            print(f"copied {source_path} to {copy_path}")

        # If we hit a directory, then we create the directory in the public folder and call the function again.
        if os.path.exists(source_path) and os.path.isdir(source_path):
            # create the new filepath
            if rel_path:
                new_dir_path = os.path.join(public_path, rel_path, file)
            else:
                new_dir_path = os.path.join(public_path, file)
            
            # If the directory doesn't exist in public, create it.
            if not os.path.isdir(new_dir_path):
                os.mkdir(new_dir_path)

            # Once directory is created, call the function again (recurse)
            recurse_copy_source_destination(source_path, static_path, public_path)
            
if __name__ == "__main__":
    main()
