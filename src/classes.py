from hashlib import sha256

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
                return False, None
            trie_node = trie_node.children[char]
        return trie_node.is_end_of_word, trie_node.node

class Node:
    def __init__(self, name=None):
        self.name = sha256(name.encode('utf-8')).hexdigest()
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
        is_end_of_word, trie_node = self.find(node)
        if is_end_of_word:
            trie_node.name = None
