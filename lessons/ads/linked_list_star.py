from lessons.ads.linked_list import LinkedList, Node


def sum_list_values(list_1: LinkedList, list_2: LinkedList) -> LinkedList:
    if list_1.len() != list_2.len():
        return None
    result_list = LinkedList()
    node_1 = list_1.head
    node_2 = list_2.head
    while node_1 is not None and node_2 is not None:
        result_node = Node(node_1.value + node_2.value)
        result_list.add_in_tail(result_node)
        node_1 = node_1.next
        node_2 = node_2.next
    return result_list
