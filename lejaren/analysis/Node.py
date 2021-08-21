class Node:
    location = None
    level = None
    children = []
    parent = []

    # I don't think we should allow init that isn't
    # either Meter or Phrase
    def __init__(self):
        if len(parent) > 1:
            print("Too many parents")

    def get_parent(self):
        return parent

    def get_siblings(self):
        return parent.children

    def get_subtree_siblings(self, node):
        head_node = node
        parent_node = get_parent()
        tree_level = 0
        neighbors = [head_node]
        children = []
        while parent_node is not head_node:
            tree_level + 1
            parent_node = get_parent(parent_node)
        # fix this with true traversal algorithm
        level = 0
        for level in range(tree_level):
            for current_neighbor in neighbors:
                children.append(get_children(current_neighbor))
            neighbors = children
            level += 1
        return neighbors

    def get_children(self):
        return children
