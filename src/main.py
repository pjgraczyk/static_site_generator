import shutil
import os
import logging
import pprint

def initialize_logger():
    ...

def delete_dest_dir(abspath):
    if not os.path.exists(abspath):
        raise ValueError(
            f'The given path of the destination directory does not exist: {path}')
    for root, dirs, files in os.walk(abspath):
        for file in files:
            ...
            # deletion_filepath = os.path.join(root, file)
        for dir in dirs:
            ...
        
            
            


def move_src_to_dest_dir(src_path, dest_dir):
    pprint(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    delete_dest_dir(os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))),
        'content',
    ))
    
if __name__ == "__main__":
    main()