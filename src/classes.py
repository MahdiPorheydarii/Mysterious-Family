from .hash import sha256
from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.node = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, node):
        trie_node = self.root
        for char in word:
            if char not in trie_node.children:
                trie_node.children[char] = TrieNode()
            trie_node = trie_node.children[char]
        trie_node.is_end_of_word = True
        trie_node.node = node

    def search(self, word):
        trie_node = self.root
        for char in word:
            if char not in trie_node.children:
                return None
            trie_node = trie_node.children[char]
        return trie_node.node
    
    def delete(self, word):
        self.delete_do(self.root, word, 0)

    def delete_do(self, current_node, word, index):
        if index == len(word):
            if current_node.is_end_of_word:
                current_node.is_end_of_word = False
                current_node.node = None
            return

        char = word[index]

        next_node = current_node.children[char]
        self.delete_do(next_node, word, index + 1)

        if not next_node.is_end_of_word and not next_node.children:
            del current_node.children[char]

class Node:
    def __init__(self, name=None):
        # self.name = sha256(name.encode("utf-8"))
        self.name = name
        self.children = []
        self.parents = []

class Tree:
    def __init__(self, root):
        self.root = root
        self.size = 1
        self.trie = Trie()
        self.trie.insert(root.name, root)

    def add(self, parent, child):
        parent.children.append(child)
        child.parents.append(parent)
        self.size += 1
        self.trie.insert(child.name, child)

    def find(self, node):
        return self.trie.search(node.name)

    def delete(self, node):
        trie_node = self.find(node)
        if trie_node:
            trie_node.name = None
            self.trie.delete(node.name)
            self.size -= 1
    
    def lca(self, node1, node2):
        visited_ancestors = set()

        def dfs_ancestors(current_node):
            visited_ancestors.add(current_node)
            for parent in current_node.parents:
                if parent not in visited_ancestors:
                    dfs_ancestors(parent)

        dfs_ancestors(node1)

        queue = deque([node2])
        while queue:
            current_node = queue.popleft()
            if current_node in visited_ancestors:
                return current_node.name
            for parent in current_node.parents:
                queue.append(parent)

        return None

    def is_related(self, node1, node2):
        ancestors1 = set()

        def get_ancestors(node, ancestors_set):
            for parent in node.parents:
                ancestors_set.add(parent)
                get_ancestors(parent, ancestors_set)

        get_ancestors(node1, ancestors1)

        for ancestor in ancestors1:
            if node2 in ancestor.children:
                return True

        ancestors2 = set()
        get_ancestors(node2, ancestors2)

        for ancestor in ancestors2:
            if node1 in ancestor.children:
                return True

        return False
    
    def farthest_child(self, node):
        if len(node.children) == 0:
            return 0

        child_heights = [self.farthest_child(child) for child in node.children if child.name != node.name]
        return 1 + max(child_heights)
