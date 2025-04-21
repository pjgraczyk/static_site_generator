from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # Check if all elements in old_nodes are instances of TextNode
    if all(isinstance(node, TextNode) for node in old_nodes):
        new_nodes = []  # Initialize a list to store the new nodes
        for node in old_nodes:
            split_nodes = []
            node_split = str.split(node.text, delimiter, 2)
            if len(node_split) > 1:
                # Create new TextNode for the part before the delimiter
                split_nodes.append(TextNode(node_split[0], text_type))
                # Create new TextNode for the delimiter itself
                split_nodes.append(TextNode(delimiter, text_type))
                # Create new TextNode for the part after the delimiter
                split_nodes.append(TextNode(node_split[1], text_type))
                # Add the split nodes to the new_nodes list
                new_nodes.extend(split_nodes)
            else:
                # Raise an error if the delimiter is not found in the node's text
                raise ValueError("Delimiter not found in node text")
        return new_nodes  # Return the list of new nodes
    else:
        # Raise an error if any element in old_nodes is not a TextNode
        raise TypeError("All nodes must be of type TextNode")
