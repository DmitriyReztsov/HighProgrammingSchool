from lessons.ads2.trees import SimpleTree, SimpleTreeNode


def test_add_child():
    root = SimpleTreeNode("root")
    tree = SimpleTree(root=root)

    child = SimpleTreeNode("child")
    tree.AddChild(root, child)

    assert child.Parent is root
    assert child in root.Children


def test_delete_node():
    root = SimpleTreeNode("root")
    child = SimpleTreeNode("child", parent=root)
    root.Children = [child]
    tree = SimpleTree(root)

    tree.DeleteNode(child)

    assert tree.Root.Children == []
    assert child.Parent is None

    tree.DeleteNode(root)

    assert tree.Root is None


def test_get_all_nodes():
    leaf_3_1 = SimpleTreeNode("3_1")
    leaf_3_2 = SimpleTreeNode("3_2")
    leaf_3_3 = SimpleTreeNode("3_3")
    leaf_3_4 = SimpleTreeNode("3_4")
    leaf_3_5 = SimpleTreeNode("3_5")
    leaf_3_6 = SimpleTreeNode("3_6")

    children_2_1 = SimpleTreeNode("2_1")
    children_2_2 = SimpleTreeNode("2_2")
    children_2_3 = SimpleTreeNode("2_3")

    root = SimpleTreeNode("root")
    tree = SimpleTree(root)

    root.Children = [children_2_1, children_2_2, children_2_3]
    children_2_1.Parent = root
    children_2_1.Children = [leaf_3_1]
    leaf_3_1.Parent = children_2_1

    children_2_2.Parent = root
    children_2_2.Children = [leaf_3_2, leaf_3_3]
    leaf_3_2.Parent = children_2_2
    leaf_3_3.Parent = children_2_2

    children_2_3.Parent = root
    children_2_3.Children = [leaf_3_4, leaf_3_5, leaf_3_6]
    leaf_3_4.Parent = children_2_3
    leaf_3_5.Parent = children_2_3
    leaf_3_6.Parent = children_2_3

    nodes_list = tree.GetAllNodes()
    refferal_nodes_list = [
        root,
        children_2_1,
        leaf_3_1,
        children_2_2,
        leaf_3_2,
        leaf_3_3,
        children_2_3,
        leaf_3_4,
        leaf_3_5,
        leaf_3_6,
    ]
    assert nodes_list == refferal_nodes_list


def test_find_node_by_value():
    leaf_3_1 = SimpleTreeNode("3_1")
    leaf_3_2 = SimpleTreeNode("test")
    leaf_3_3 = SimpleTreeNode("3_3")
    leaf_3_4 = SimpleTreeNode("3_4")
    leaf_3_5 = SimpleTreeNode("test")
    leaf_3_6 = SimpleTreeNode("3_6")

    children_2_1 = SimpleTreeNode("2_1")
    children_2_2 = SimpleTreeNode("test")
    children_2_3 = SimpleTreeNode("2_3")

    root = SimpleTreeNode("root")
    tree = SimpleTree(root)

    root.Children = [children_2_1, children_2_2, children_2_3]
    children_2_1.Parent = root
    children_2_1.Children = [leaf_3_1]
    leaf_3_1.Parent = children_2_1

    children_2_2.Parent = root
    children_2_2.Children = [leaf_3_2, leaf_3_3]
    leaf_3_2.Parent = children_2_2
    leaf_3_3.Parent = children_2_2

    children_2_3.Parent = root
    children_2_3.Children = [leaf_3_4, leaf_3_5, leaf_3_6]
    leaf_3_4.Parent = children_2_3
    leaf_3_5.Parent = children_2_3
    leaf_3_6.Parent = children_2_3

    found_nodes = tree.FindNodesByValue("test")
    refferal_found_nodes = [children_2_2, leaf_3_2, leaf_3_5]

    assert found_nodes == refferal_found_nodes


def test_move_node():
    leaf_3_1 = SimpleTreeNode("3_1")
    leaf_3_2 = SimpleTreeNode("3_2")
    leaf_3_3 = SimpleTreeNode("3_3")
    leaf_3_4 = SimpleTreeNode("3_4")
    leaf_3_5 = SimpleTreeNode("3_5")
    leaf_3_6 = SimpleTreeNode("3_6")

    children_2_1 = SimpleTreeNode("2_1")
    children_2_2 = SimpleTreeNode("2_2")
    children_2_3 = SimpleTreeNode("2_3")

    root = SimpleTreeNode("root")
    tree = SimpleTree(root)

    root.Children = [children_2_1, children_2_2, children_2_3]
    children_2_1.Parent = root
    children_2_1.Children = [leaf_3_1]
    leaf_3_1.Parent = children_2_1

    children_2_2.Parent = root
    children_2_2.Children = [leaf_3_2, leaf_3_3]
    leaf_3_2.Parent = children_2_2
    leaf_3_3.Parent = children_2_2

    children_2_3.Parent = root
    children_2_3.Children = [leaf_3_4, leaf_3_5, leaf_3_6]
    leaf_3_4.Parent = children_2_3
    leaf_3_5.Parent = children_2_3
    leaf_3_6.Parent = children_2_3

    tree.MoveNode(children_2_3, children_2_1)
    all_nodes = tree.GetAllNodes()
    refferal_all_nodes = [
        root,
        children_2_1,
        leaf_3_1,
        children_2_3,
        leaf_3_4,
        leaf_3_5,
        leaf_3_6,
        children_2_2,
        leaf_3_2,
        leaf_3_3,
    ]

    assert all_nodes == refferal_all_nodes


def test_count_all_n_leaves():
    leaf_3_1 = SimpleTreeNode("3_1")
    leaf_3_2 = SimpleTreeNode("3_2")
    leaf_3_3 = SimpleTreeNode("3_3")
    leaf_3_4 = SimpleTreeNode("3_4")
    leaf_3_5 = SimpleTreeNode("3_5")
    leaf_3_6 = SimpleTreeNode("3_6")

    children_2_1 = SimpleTreeNode("2_1")
    children_2_2 = SimpleTreeNode("2_2")
    children_2_3 = SimpleTreeNode("2_3")

    root = SimpleTreeNode("root")
    tree = SimpleTree(root)

    root.Children = [children_2_1, children_2_2, children_2_3]
    children_2_1.Parent = root
    children_2_1.Children = [leaf_3_1]
    leaf_3_1.Parent = children_2_1

    children_2_2.Parent = root
    children_2_2.Children = [leaf_3_2, leaf_3_3]
    leaf_3_2.Parent = children_2_2
    leaf_3_3.Parent = children_2_2

    children_2_3.Parent = root
    children_2_3.Children = [leaf_3_4, leaf_3_5, leaf_3_6]
    leaf_3_4.Parent = children_2_3
    leaf_3_5.Parent = children_2_3
    leaf_3_6.Parent = children_2_3

    assert tree.Count() == 10
    assert tree.LeafCount() == 6
