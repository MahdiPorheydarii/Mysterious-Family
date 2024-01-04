from classes import Tree, Node

def family():
    john = Node("John")
    jane = Node("Jane")
    bob = Node("Bob")
    alice = Node("Alice")
    Loo = Node("Loo")
    Boo = Node("Boo")

    family_tree = Tree(john)
    family_tree.add(john, jane)
    family_tree.add(john, bob)
    family_tree.add(jane, alice)
    family_tree.add(john, Boo)
    family_tree.add(john, Loo)
    
    return family_tree
