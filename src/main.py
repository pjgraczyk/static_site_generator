import markdown_utils

def main():
    md = """
    ## Heading 1
    
    1. Heading 1
    
    
    This is a code block

    ```
    def hello_world():
        print("Hello, world!")
    ```
    
    > This is a quote
    
    - Item 1
    - Item 2
    - Item 3
    
    """
    print(markdown_utils.markdown_to_html(md))

if __name__ == "__main__":
    main()
