class Node:
    def __init__(self, hash=None):
        self.hash = hash
        self.children = []
        self.parents = []

class Tree:
    def __init__(self, root):
        self.root = root

    def add(self, parent, child):
        parent.children.append(child)
        child.parents.append(parent)
