# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> ListNode | None:
        node_a = headA
        visited_set = set()
        while node_a.next:
            visited_set.add(node_a)
            node_a = node_a.next
        visited_set.add(node_a)

        node_b = headB
        while node_b.next:
            if node_b in visited_set:
                return node_b
            visited_set.add(node_b)
            node_b = node_b.next

        if node_b in visited_set:
            return node_b

        return None

    def _getIntersectionNode(
        self, headA: ListNode, headB: ListNode
    ) -> ListNode | None:
        """на второй итерации, в случае разных длин списков, указатели
        сойдутся. Либо на общем узле, либо на значении None, что будет
        означать конец списка.
        """

        head_a = headA
        head_b = headB
        while head_a != head_b:
            head_a = head_a.next if head_a else headB
            head_b = head_b.next if head_b else headA

        return head_a


if __name__ == "__main__":
    intersectVal = 8
    listA = [4, 1, 8, 4, 5]
    listB = [5, 6, 1, 8, 4, 5]
    skipA = 2
    skipB = 3

    nodes_a = []
    nodes_b = []
    nodes_common = []
    prev_node = None
    for ind_a in range(skipA):
        node = ListNode(listA[ind_a])
        if prev_node:
            prev_node.next = node
        prev_node = node
        nodes_a.append(node)

    prev_node = None
    for ind_b in range(skipB):
        node = ListNode(listB[ind_b])
        if prev_node:
            prev_node.next = node
        prev_node = node
        nodes_b.append(node)

    prev_node = None
    if ind_a + 1 < len(listA) and ind_b + 1 < len(listB):
        prev_node_a = nodes_a[-1]
        prev_node_b = nodes_b[-1]
        for ind_common in range(ind_b + 1, len(listB)):
            node = ListNode(listB[ind_common])
            if not prev_node:
                prev_node_a.next = node
                prev_node_b.next = node
            else:
                prev_node.next = node
            prev_node = node
            nodes_common.append(node)

    print(Solution().getIntersectionNode(nodes_a[0], nodes_b[0]))
