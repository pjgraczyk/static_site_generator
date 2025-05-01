import markdown_utils

def main():
    md = ""    
    print(markdown_utils.markdown_to_blocks(md))
    print(markdown_utils.block_to_block_type(md))

if __name__ == "__main__":
    main()
