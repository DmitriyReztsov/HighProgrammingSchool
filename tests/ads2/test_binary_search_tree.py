from lessons.ads2.binary_search_tree import BST, BSTFind, BSTNode


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


def test_search():
    tree = BST(root_8)

    result = tree.FindNodeByKey(10)
    assert isinstance(result, BSTFind)
    assert result.Node == child_10
    assert result.NodeHasKey is True
    assert result.ToLeft is False

    result = tree.FindNodeByKey(7)
    assert isinstance(result, BSTFind)
    assert result.Node == child_6
    assert result.NodeHasKey is False
    assert result.ToLeft is False

    result = tree.FindNodeByKey(13)
    assert isinstance(result, BSTFind)
    assert result.Node == child_14
    assert result.NodeHasKey is False
    assert result.ToLeft is True


def test_add():
    tree = BST(root_8)

    search_before = tree.FindNodeByKey(5)
    added = tree.AddKeyValue(5, "5")
    search_after = tree.FindNodeByKey(5)
    assert search_before.NodeHasKey is False
    assert search_before.ToLeft is True
    assert added is True
    assert search_after.NodeHasKey is True

    search_before = tree.FindNodeByKey(7)
    added = tree.AddKeyValue(7, "7")
    search_after = tree.FindNodeByKey(7)
    assert search_before.NodeHasKey is False
    assert search_before.ToLeft is False
    assert added is True
    assert search_after.NodeHasKey is True

    search_before = tree.FindNodeByKey(6)
    added = tree.AddKeyValue(6, "6")
    search_after = tree.FindNodeByKey(6)
    assert search_before.NodeHasKey is True
    assert search_before.ToLeft is False
    assert added is False
    assert search_after.NodeHasKey is True


def test_max_min():
    tree = BST(root_8)

    max_node = tree.FinMinMax(tree.Root, True)
    min_node = tree.FinMinMax(tree.Root, False)
    assert max_node.NodeValue == "14"
    assert min_node.NodeValue == "1"

    max_node = tree.FinMinMax(child_4, True)
    min_node = tree.FinMinMax(child_4, False)
    assert max_node.NodeValue == "6"
    assert min_node.NodeValue == "1"

    max_node = tree.FinMinMax(child_14, True)
    min_node = tree.FinMinMax(child_14, False)
    assert max_node.NodeValue == min_node.NodeValue == "14"


def test_delete():
    tree = BST(root_8)

    deleted = tree.DeleteNodeByKey(9)
    assert deleted is True
    assert child_10.LeftChild is None
    assert child_10.RightChild is None
    assert child_9.Parent is None

    tree_2 = BST(child_1)
    deleted = tree_2.DeleteNodeByKey(9)
    assert deleted is False

    deleted = tree_2.DeleteNodeByKey(1)
    assert deleted is True
    assert tree_2.Root is None

    child_10.LeftChild = child_9
    child_9.Parent = child_10
    deleted = tree.DeleteNodeByKey(10)
    assert deleted is True
    assert child_12.LeftChild is child_9
    assert child_9.Parent is child_12
    assert child_10.Parent is None
    assert child_10.LeftChild is None

    child_12.LeftChild = child_10
    child_10.Parent = child_12
    child_10.LeftChild = child_9
    child_9.Parent = child_10
    deleted = tree.DeleteNodeByKey(8)
    assert deleted is True
    assert root_8.LeftChild is None
    assert root_8.RightChild is None
    assert child_9.LeftChild is child_4
    assert child_9.RightChild is child_12
    assert child_4.Parent is child_9
    assert child_12.Parent is child_9
    assert child_10.LeftChild is None
    assert child_9.Parent is None
    assert tree.Root is child_9


def test_count_tree():
    tree = BST(root_8)
    assert tree.Count() == 10

    tree = BST(child_1)
    assert tree.Count() == 1

    tree = BST()
    assert tree.Count() == 0
