from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    CODE = "code"
    SUBSCRIPT = "subscript"
    SUPERSCRIPT = "superscript"
    QUOTE = "quote"
    BLOCKQUOTE = "blockquote"
    CODEBLOCK = "codeblock"
    UNORDEREDLIST = "unorderedlist"
    ORDEREDLIST = "orderedlist"
    LISTITEM = "listitem"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"
    HEADING4 = "heading4"
    HEADING5 = "heading5"
    HEADING6 = "heading6"
    PARAGRAPH = "paragraph"
    LINK = "link"
    IMAGE = "image"
    TABLE = "table"
    TABLEROW = "tablerow"


class TextNode:
    def __init__(self, text, text_type, url=None, alt=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.alt = alt

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f'TextNode("{self.text}", {self.text_type}, "{self.url}")'

    def text_node_to_html_node(self, text_node):
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text)
            case TextType.BOLD:
                return LeafNode(tag="b", value=text_node.text)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text)
            case TextType.CODE:
                return LeafNode(tag="code", value=text_node.text)
            case TextType.LINK:
                return LeafNode(
                    tag="a",
                    value=text_node.text,
                    props={"href": text_node.url},
                )
            case TextType.IMAGE:
                if text_node.alt is None:
                    raise ValueError("Alt text is required for images")
                if text_node.url is None:
                    raise ValueError("Url source is required for images")
                return LeafNode(
                    tag="img",
                    value="",
                    props={"alt": text_node.alt, "src": text_node.url},
                )
            case _:
                raise ValueError(f"Unknown text type: {text_node.text_type}")
