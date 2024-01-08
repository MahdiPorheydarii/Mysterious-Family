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