from libs.hash import sha256
from collections import deque
from .Trie import Trie

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
        if not self.find(child):
            self.size += 1
        self.trie.insert(child.name, child)
        if self.find(parent) == None:
            self.trie.insert(parent.name, parent)
            self.size += 1

    def find(self, node):
        return self.trie.search(node.name)

    def delete(self, node):
        trie_node = self.find(node)
        if trie_node:
            self.trie.delete(node.name)
            trie_node.name = None
            self.size -= 1
    
    def lca(self, node1, node2):
        if node1 == None or node2 == None:
            return None
        
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

    def are_related(self, node1, node2):
        tmp = self.find(Node(self.lca(node1, node2)))
        return tmp and node1 != tmp and node2 != tmp
    
    def farthest_child(self, node):
        if len(node.children) == 0:
            return 0

        child_heights = [self.farthest_child(child) for child in node.children if child.name != node.name]
        return 1 + max(child_heights)
    
    def import_tree(self, root, pairs):
        self.root = Node(root)
        self.trie = Trie()
        self.trie.insert(root, self.root)
        self.size = 1

        pairs = [i.split() for i in pairs]
        pairs = pairs[0:-1] if pairs[-1] == [] else pairs

        for i in pairs:
            tmp = self.find(Node(i[1]))
            if tmp:
                self.add(self.find(Node(i[0])), tmp)
            else:
                self.add(self.find(Node(i[0])), Node(i[1]))
        
    def is_ancestor(self, node1, node2):
        if node1 == None or node2 == []:
            return False
        if node1 in [j for x in node2 for j in x.parents]:
            return True
        return self.is_ancestor(node1, [j for x in node2 for j in x.parents])
    
    def is_siblings(self,node1, node2):
        return (node1 in [x for j in node2.parents for x in j.children]) or (node2 in [x for j in node1.parents for x in j.children])
    
    def two_furthest(self):
        def dfs(node, distances, visited):
            visited.add(node)
            
            if not node.children:
                distances[node] = 0
                return 0, node

            farthest = None
            max_dist = 0

            for child in node.children:
                if child not in visited:
                    dist, child_leaf = dfs(child, distances, visited)
                    if dist + 1 > max_dist:
                        max_dist = dist + 1
                        farthest = child_leaf

            distances[node] = max_dist
            return max_dist, farthest

        distances_from_root = {}
        _, farthest = dfs(self.root, distances_from_root, set())
        
        _, far2 = dfs(self.root, distances_from_root, set(self.one_root([farthest])))
        
        return farthest.name, far2.name
    
    
    def one_root(self, node):
        if self.root in [x for j in node for x in j.parents]:
            return node
        return self.one_root([x for j in node for x in j.parents])

    def to_txt(self):
        with open("Tree.txt", "w") as file:
            root = "_".join(self.root.name.split())
            file.write(f"{root}\n")
            
            queue = deque([self.root])
            while(queue):
                node = queue.popleft()
                for i in node.children:
                    name = "_".join(i.name.split())
                    parent = "_".join(node.name.split())
                    file.write(f"{parent} {name}\n")
                for i in node.children:
                    queue.append(i)