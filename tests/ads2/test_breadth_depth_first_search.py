from lessons.ads2.breadth_depth_first_search import BST, BSTNode


root_8 = BSTNode(8, "8")
child_4 = BSTNode(4, "4")
child_12 = BSTNode(12, "12")
child_2 = BSTNode(2, "2")
child_6 = BSTNode(6, "6")
child_10 = BSTNode(10, "10")
child_14 = BSTNode(14, "14")
child_1 = BSTNode(1, "1")
child_3 = BSTNode(3, "3")
child_9 = BSTNode(9, "9")

root_8.LeftChild = child_4
child_4.Parent = root_8
root_8.RightChild = child_12
child_12.Parent = root_8

child_4.LeftChild = child_2
child_2.Parent = child_4
child_4.RightChild = child_6
child_6.Parent = child_4

child_12.LeftChild = child_10
child_10.Parent = child_12
child_12.RightChild = child_14
child_14.Parent = child_12

child_2.LeftChild = child_1
child_1.Parent = child_2
child_2.RightChild = child_3
child_3.Parent = child_2

child_10.LeftChild = child_9
child_9.Parent = child_10


def test_breadth_first_search():
    tree = BST(root_8)

    breadth_result = tree.WideAllNodes()
    reference_list = [
        root_8,
        child_4,
        child_12,
        child_2,
        child_6,
        child_10,
        child_14,
        child_1,
        child_3,
        child_9,
    ]

    assert breadth_result == reference_list


def test_depth_first_search():
    tree = BST(root_8)

    depth_list = tree.DeepAllNodes(0)
    reference_list = [
        child_1,
        child_2,
        child_3,
        child_4,
        child_6,
        root_8,
        child_9,
        child_10,
        child_12,
        child_14,
    ]
    assert depth_list == reference_list

    depth_list = tree.DeepAllNodes(1)
    reference_list = [
        child_1,
        child_3,
        child_2,
        child_6,
        child_4,
        child_9,
        child_10,
        child_14,
        child_12,
        root_8,
    ]
    assert depth_list == reference_list

    depth_list = tree.DeepAllNodes(2)
    reference_list = [
        root_8,
        child_4,
        child_2,
        child_1,
        child_3,
        child_6,
        child_12,
        child_10,
        child_9,
        child_14,
    ]
    assert depth_list == reference_list
