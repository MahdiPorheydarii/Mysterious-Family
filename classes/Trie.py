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

