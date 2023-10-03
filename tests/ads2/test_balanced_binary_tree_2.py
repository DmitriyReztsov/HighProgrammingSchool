from lessons.ads2.balanced_binary_tree_2 import BSTNode, BalancedBST


input_array = [25, 31, 37, 43, 50, 55, 62, 75, 84, 92, 95, 100, 102, 109]  # , 115]


def test_generate():
    tree = BalancedBST()

    root = tree.GenerateTree(input_array)
    assert root.NodeKey == 75
    assert root.LeftChild.NodeKey == 43
    assert root.RightChild.NodeKey == 100
    assert root.LeftChild.LeftChild.Level == 2
    assert root.RightChild.LeftChild.RightChild.Level == 3


def test_is_balanced():
    tree = BalancedBST()
    root = tree.GenerateTree(input_array)

    is_balanced = tree.IsBalanced(root)
    assert is_balanced is True

    root = BSTNode(50)
    child1 = BSTNode(25, root)
    child2 = BSTNode(75, root)

    child12 = BSTNode(37, child1)
    child1.RightChild = child12
    child21 = BSTNode(62, child2)
    child2.LeftChild = child21
    child22 = BSTNode(84, child2)
    child2.RightChild = child22

    child121 = BSTNode(31, child12)
    child12.LeftChild = child121
    child122 = BSTNode(43, child12)
    child12.RightChild = child122

    child211 = BSTNode(55, child21)
    child21.LeftChild = child211
    child222 = BSTNode(92, child22)
    child22.RightChild = child222

    tree = BalancedBST()
    tree.Root = root

    assert tree.IsBalanced(root) is False
