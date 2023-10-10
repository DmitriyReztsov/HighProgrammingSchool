from lessons.ads2.even_trees import SimpleTree, SimpleTreeNode


def test_even_trees():
    tree = SimpleTree()
    root = SimpleTreeNode(1)
    tree.Root = root

    child_2 = SimpleTreeNode(2, root)
    child_3 = SimpleTreeNode(3, root)
    child_6 = SimpleTreeNode(6, root)
    root.Children = [child_2, child_3, child_6]

    child_5 = SimpleTreeNode(5, child_2)
    child_7 = SimpleTreeNode(7, child_2)
    child_2.Children = [child_5, child_7]

    child_4 = SimpleTreeNode(4, child_3)
    child_3.Children = [child_4]

    child_8 = SimpleTreeNode(8, child_6)
    child_6.Children = [child_8]

    child_9 = SimpleTreeNode(9, child_8)
    child_10 = SimpleTreeNode(10, child_8)
    child_8.Children = [child_9, child_10]

    make_forest_list = tree.EvenTrees()
    assert make_forest_list == [root, child_6, root, child_3] or make_forest_list == [
        root,
        child_3,
        root,
        child_6,
    ]
