from hash import sha256

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

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
        self.trie.insert(child.name)
    
    def find(self, Trie : Trie, node):
        return self.trie.search(node.name)

    def delete(self, node):
        if(self.find(node)):
            pass
