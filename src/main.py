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
    html_nodes = markdown_utils.markdown_to_html_node(md)
    html = html_nodes.to_html()
    print(html)
if __name__ == "__main__":
    main()
