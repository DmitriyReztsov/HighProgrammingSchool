from lessons.ads2.binary_search_tree_2 import aBST


nodes_list = [
    50,
    25,
    75,
    None,
    37,
    62,
    84,
    None,
    None,
    31,
    43,
    55,
    None,
    None,
    92,
]


def test_search():
    tree = aBST(3)

    assert len(tree.Tree) == 15

    tree.Tree = nodes_list

    assert tree.FindKeyIndex(50) == 0
    assert tree.FindKeyIndex(43) == 10
    assert tree.FindKeyIndex(20) == -3
    assert tree.FindKeyIndex(100) is None

    tree = aBST()

    assert tree.FindKeyIndex(1) is None

    tree = aBST(0)

    assert tree.FindKeyIndex(1) == 0


def test_add():
    tree = aBST(3)
    tree.Tree = nodes_list

    assert tree.AddKey(20) == 3
    assert tree.FindKeyIndex(20) == 3
    assert tree.AddKey(92) == 14
    assert tree.FindKeyIndex(92) == 14
    assert tree.AddKey(100) == -1

    tree = aBST()
    assert tree.AddKey(1) == -1

    tree = aBST(1)
    assert tree.AddKey(1) == 0
    assert tree.AddKey(2) == 2
