from textnode import TextNode


def split_nodes_delimiter(nodes, delimiter, new_type):
    result = []
    for node in nodes:
        if not isinstance(node, TextNode):
            raise TypeError("Expected a TextNode")

        text = node.text if node.text is not None else ""

        parts = text.split(delimiter)

        if len(parts) == 1:
            result.append(node)
            continue
        elif len(parts) == 2:
            result.append(TextNode(parts[0], node.text_type))
            result.append(TextNode(parts[1], node.text_type))
            continue
        else:
            for i, part in enumerate(parts):
                if not part:
                    continue

                current_type = node.text_type if i % 2 == 0 else new_type
                result.append(TextNode(part, current_type))

    return result
