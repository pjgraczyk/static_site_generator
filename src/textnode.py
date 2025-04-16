from enum import Enum


class TextType(Enum):
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
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
