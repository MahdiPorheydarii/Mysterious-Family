from ..classes.Tree import Tree, Node

def family():
    Mahdi = Node("Mahdi the Almighty")
    John = Node("John")
    Jane = Node("Jane")
    Bob = Node("Bob")
    alice = Node("Alice")
    Loo = Node("Loo")
    Boo = Node("Boo")
    Koo = Node("Koo")
    Joo = Node("Joo")
    Sarah = Node("Sarah")

    family_tree = Tree(Mahdi)
    family_tree.add(Mahdi, John)
    family_tree.add(Mahdi, Jane)
    family_tree.add(Jane, alice)
    family_tree.add(John, Boo)
    family_tree.add(John, Loo)
    family_tree.add(Loo, Koo)
    family_tree.add(Loo, Joo)
    family_tree.add(Jane, Sarah)
    
    return family_tree

fam = family()