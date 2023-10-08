from lessons.ads2.graph import Vertex, SimpleGraph


def test_add():
    graph = SimpleGraph(5)

    assert all([x is None for x in graph.vertex])

    new_vertex = graph.AddVertex(1)

    assert not all([x is None for x in graph.vertex])
    assert new_vertex in graph.vertex

    index_new_vertex = graph.vertex.index(new_vertex)
    assert all([x == 0 for x in graph.m_adjacency[index_new_vertex]])
    assert all(x[index_new_vertex] == 0 for x in graph.m_adjacency)

    new_vertex = graph.AddVertex(2)

    assert new_vertex in graph.vertex

    index_new_vertex = graph.vertex.index(new_vertex)
    assert all([x == 0 for x in graph.m_adjacency[index_new_vertex]])
    assert all(x[index_new_vertex] == 0 for x in graph.m_adjacency)

    new_vertex = graph.AddVertex(3)
    new_vertex = graph.AddVertex(4)
    new_vertex = graph.AddVertex(5)
    new_vertex = graph.AddVertex(6)

    assert new_vertex is None


def test_add_edge():
    graph = SimpleGraph(5)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)

    graph.AddEdge(new_vertex_1, new_vertex_2)
    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)

    assert graph.m_adjacency[ind_1][ind_2] == graph.m_adjacency[ind_2][ind_1] == 1

    graph.AddEdge(new_vertex_1, new_vertex_3)
    ind_1 = graph.vertex.index(new_vertex_1)
    ind_3 = graph.vertex.index(new_vertex_3)

    assert graph.m_adjacency[ind_1][ind_3] == graph.m_adjacency[ind_3][ind_1] == 1

    assert graph.m_adjacency[ind_2][ind_3] == graph.m_adjacency[ind_3][ind_2] == 0


def test_is_edge():
    graph = SimpleGraph(5)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)

    graph.AddEdge(new_vertex_1, new_vertex_2)
    graph.AddEdge(new_vertex_1, new_vertex_3)
    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)
    ind_3 = graph.vertex.index(new_vertex_3)

    assert graph.IsEdge(new_vertex_1, new_vertex_2)
    assert graph.IsEdge(new_vertex_2, new_vertex_1)
    assert graph.IsEdge(new_vertex_1, new_vertex_3)
    assert graph.IsEdge(new_vertex_3, new_vertex_1)
    assert not graph.IsEdge(new_vertex_2, new_vertex_2)
    assert not graph.IsEdge(new_vertex_3, new_vertex_2)
    assert not graph.IsEdge(new_vertex_2, new_vertex_3)


def test_remove_edge():
    graph = SimpleGraph(5)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)

    graph.AddEdge(new_vertex_1, new_vertex_2)
    graph.AddEdge(new_vertex_1, new_vertex_3)
    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)
    ind_3 = graph.vertex.index(new_vertex_3)

    graph.RemoveEdge(new_vertex_1, new_vertex_3)
    graph.RemoveEdge(new_vertex_2, new_vertex_3)

    assert not graph.IsEdge(new_vertex_2, new_vertex_2)
    assert not graph.IsEdge(new_vertex_3, new_vertex_2)
    assert not graph.IsEdge(new_vertex_2, new_vertex_3)
    assert not graph.IsEdge(new_vertex_1, new_vertex_3)
    assert not graph.IsEdge(new_vertex_3, new_vertex_1)
    assert graph.IsEdge(new_vertex_2, new_vertex_1)


def test_remove_vertex():
    graph = SimpleGraph(5)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)
    new_vertex_3 = graph.AddVertex(4)
    new_vertex_3 = graph.AddVertex(5)

    graph.AddEdge(new_vertex_1, new_vertex_2)
    graph.AddEdge(new_vertex_1, new_vertex_3)
    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)
    ind_3 = graph.vertex.index(new_vertex_3)

    assert graph.empty_vertex_index == -1
    graph.RemoveVertex(new_vertex_2)

    assert new_vertex_2 not in graph.vertex
    assert graph.vertex[ind_2] is None
    assert graph.m_adjacency[ind_1][ind_2] == graph.m_adjacency[ind_2][ind_1] == 0

    assert graph.empty_vertex_index == 4
