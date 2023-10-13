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

        self._find_way_dfs(vertex_stack, VFrom, Vto)
        return vertex_stack

    def _find_way_dfs(
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
            search_result = self._find_way_dfs(v_stack, index, v_to_index)
            if search_result == v_to_index:
                return search_result

        # no children or all children are hit
        if search_result is None:
            v_stack.pop(-1)
        return search_result

    def BreadthFirstSearch(self, VFrom: int, VTo: int) -> List[Vertex]:
        # узлы задаются позициями в списке vertex
        # возвращается список узлов -- путь из VFrom в VTo
        # или [] если пути нету
        for vertex in self.vertex:
            if vertex is None:
                continue
            vertex.hit = False

        return self._find_way_bfs(VFrom, VTo)

    def _find_way_bfs(self, v_from_index: int, v_to_index: int) -> List[Vertex]:
        self.vertex[v_from_index].hit = True
        v_queue = [v_from_index]
        way_matrix = [[None] * self.max_vertex for _ in range(self.max_vertex)]
        current_level = 0
        for i in range(self.max_vertex):
            way_matrix[i][i] = current_level

        while v_queue:
            aux_queue = []
            current_level += 1
            for index in v_queue:
                for child_index, is_edge in enumerate(self.m_adjacency[index]):
                    if not is_edge or self.vertex[child_index].hit:
                        continue
                    self.vertex[child_index].hit = True
                    way_matrix[index][child_index] = way_matrix[child_index][
                        index
                    ] = current_level
                    aux_queue.append(child_index)
                    if child_index == v_to_index:
                        return self._restore_way(way_matrix, v_to_index)
                v_queue = aux_queue
        return []

    def _restore_way(
        self, way_matrix: List[List[int]], v_to_index: int
    ) -> List[Vertex]:
        for cell_index, level in enumerate(way_matrix[v_to_index]):
            if level is not None and level != 0:
                break
        way_list = [v_to_index, cell_index]
        v_to_index = cell_index
        search_level = level - 1
        while search_level > 0:
            for cell_index, level in enumerate(way_matrix[v_to_index]):
                if level == search_level:
                    way_list.append(cell_index)
                    v_to_index = cell_index
                    search_level -= 1
                    break
        return self._trim_way_list(way_list)

    def _trim_way_list(self, way_list_indexes: List[int]) -> List[Vertex]:
        way_list = []
        for index in reversed(way_list_indexes):
            way_list.append(self.vertex[index])
        return way_list
