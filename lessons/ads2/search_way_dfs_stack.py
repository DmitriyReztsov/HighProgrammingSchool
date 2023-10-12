from typing import Any, List


class Vertex:
    def __init__(self, val: Any) -> None:
        self.Value = val
        self.hit = False


class SimpleGraph:
    def __init__(self, size: int) -> None:
        self.max_vertex = size
        self.m_adjacency: List[List[int]] = [[0] * size for _ in range(size)]
        self.vertex: List[Vertex | None] = [None] * size

    @property
    def empty_vertex_index(self):
        for index, value in enumerate(self.vertex):
            if value is None:
                return index
        return -1

    def AddVertex(self, v: Any) -> Vertex:
        # добавление новой вершины
        # с значением v
        # в свободное место массива vertex
        if self.empty_vertex_index == -1:
            return
        new_vertex = Vertex(v)
        self.vertex[self.empty_vertex_index] = new_vertex
        return new_vertex

    # здесь и далее, параметры v -- индекс вершины
    # в списке  vertex
    def RemoveVertex(self, v: int) -> None:
        # код удаления вершины со всеми её рёбрами
        if v >= self.max_vertex:
            return
        for vert_index, vert in enumerate(self.vertex):
            if vert is not None:
                self.RemoveEdge(v, vert_index)

        self.vertex[v] = None

    def IsEdge(self, v1: int, v2: int) -> bool:
        # True если есть ребро между вершинами v1 и v2
        if v1 >= self.max_vertex or v2 >= self.max_vertex:
            return False

        return self.m_adjacency[v1][v2] == self.m_adjacency[v2][v1] == 1

    def AddEdge(self, v1: int, v2: int) -> None:
        # добавление ребра между вершинами v1 и v2
        if v1 >= self.max_vertex or v2 >= self.max_vertex:
            return
        if self.vertex[v1] is None or self.vertex[v2] is None:
            return
        self.m_adjacency[v1][v2] = self.m_adjacency[v2][v1] = 1

    def RemoveEdge(self, v1: int, v2: int) -> None:
        # удаление ребра между вершинами v1 и v2
        if v1 >= self.max_vertex or v2 >= self.max_vertex:
            return
        if self.vertex[v1] is None or self.vertex[v2] is None:
            return
        self.m_adjacency[v1][v2] = self.m_adjacency[v2][v1] = 0

    def DepthFirstSearch(self, VFrom: int, Vto: int) -> List[Vertex]:
        vertex_stack = []
        for vertex in self.vertex:
            if vertex is None:
                continue
            vertex.hit = False

        self._find_way(vertex_stack, VFrom, Vto)
        return vertex_stack

    def _find_way(
        self, v_stack: List[Vertex], v_from_index: int, v_to_index: int
    ) -> None:
        v_from = self.vertex[v_from_index]
        v_stack.append(v_from)
        v_from.hit = True

        if self.IsEdge(v_from_index, v_to_index):
            v_stack.append(self.vertex[v_to_index])
            return v_to_index

        search_result = None
        for index, value in enumerate(self.m_adjacency[v_from_index]):
            if value == 0 or self.vertex[index].hit:
                continue
            search_result = self._find_way(v_stack, index, v_to_index)
            if search_result == v_to_index:
                return search_result

        # no children or all children are hit
        if search_result is None:
            v_stack.pop(-1)
        return search_result
