from node_utils import text_to_textnodes
from pprintpp import pprint as pp


def main():
    text_to_process = [
        "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    ]
    for text in text_to_process:
        print()
        pp(f"Processing text: {text}")
        pp(text_to_textnodes(text))


if __name__ == "__main__":
    main()
