from lessons.ads2.balanced_binary_tree import GenerateBBSTArray


def test_balance_tree():
    input_array = [25, 31, 37, 43, 50, 55, 62, 75, 84, 92, 95, 100, 102, 109, 115]

    balanced_array = GenerateBBSTArray(input_array)
    reference_balanced = [
        75, 43, 100, 31, 55, 92, 109, 25, 37, 50, 62, 84, 95, 102, 115
    ]
    assert balanced_array == reference_balanced

    input_array = [25]
    reference_balanced = [25]
    assert reference_balanced == GenerateBBSTArray(input_array)
    