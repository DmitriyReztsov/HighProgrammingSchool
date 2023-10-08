from typing import Any, List


class Vertex:
    def __init__(self, val: Any) -> None:
        self.Value = val


class SimpleGraph:
    def __init__(self, size: int) -> None:
        self.max_vertex = size
        self.m_adjacency: List[List[int]] = [[0] * size for _ in range(size)]
        self.vertex: List[Vertex | None] = [None] * size
        self.empty_vertex_index = 0

    def AddVertex(self, v: Any) -> Vertex:
        # ваш код добавления новой вершины
        # с значением value
        # в свободное место массива vertex
        if self.empty_vertex_index == -1:
            return
        new_vertex = Vertex(v)
        self.vertex[self.empty_vertex_index] = new_vertex
        self.empty_vertex_index = (
            self.empty_vertex_index + 1
            if self.empty_vertex_index < self.max_vertex - 1
            else -1
        )
        return new_vertex

    # здесь и далее, параметры v -- индекс вершины
    # в списке  vertex
    def RemoveVertex(self, v: Vertex) -> None:
        if not v in self.vertex:
            return
        # ваш код удаления вершины со всеми её рёбрами
        for vert in self.vertex:
            self.RemoveEdge(v, vert)

        index_v = self.vertex.index(v)
        self.vertex[index_v] = None

        self.empty_vertex_index = (
            self.empty_vertex_index - 1
            if self.empty_vertex_index != -1
            else self.max_vertex - 1
        )

    def IsEdge(self, v1: Vertex, v2: Vertex) -> bool:
        # True если есть ребро между вершинами v1 и v2
        if not (v1 in self.vertex and v2 in self.vertex):
            return False
        index_1 = self.vertex.index(v1)
        index_2 = self.vertex.index(v2)
        return (
            self.m_adjacency[index_1][index_2]
            == self.m_adjacency[index_2][index_1]
            == 1
        )

    def AddEdge(self, v1: Vertex, v2: Vertex) -> None:
        if not (v1 in self.vertex and v2 in self.vertex):
            return
        # добавление ребра между вершинами v1 и v2
        index_1 = self.vertex.index(v1)
        index_2 = self.vertex.index(v2)
        self.m_adjacency[index_1][index_2] = self.m_adjacency[index_2][index_1] = 1

    def RemoveEdge(self, v1: Vertex, v2: Vertex) -> None:
        if not (v1 in self.vertex and v2 in self.vertex):
            return
        # удаление ребра между вершинами v1 и v2
        index_1 = self.vertex.index(v1)
        index_2 = self.vertex.index(v2)
        self.m_adjacency[index_1][index_2] = self.m_adjacency[index_2][index_1] = 0
