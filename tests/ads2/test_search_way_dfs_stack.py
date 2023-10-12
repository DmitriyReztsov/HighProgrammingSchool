from lessons.ads2.search_way_dfs_stack import SimpleGraph, Vertex


def test_search_way():
    graph = SimpleGraph(6)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)
    new_vertex_4 = graph.AddVertex(4)
    new_vertex_5 = graph.AddVertex(5)
    new_vertex_6 = graph.AddVertex(6)

    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)
    ind_3 = graph.vertex.index(new_vertex_3)
    ind_4 = graph.vertex.index(new_vertex_4)
    ind_5 = graph.vertex.index(new_vertex_5)
    ind_6 = graph.vertex.index(new_vertex_6)

    graph.AddEdge(ind_1, ind_2)
    graph.AddEdge(ind_3, ind_1)
    graph.AddEdge(ind_3, ind_4)
    graph.AddEdge(ind_4, ind_2)
    graph.AddEdge(ind_1, ind_5)
    graph.AddEdge(ind_5, ind_2)
    graph.AddEdge(ind_5, ind_3)
    graph.AddEdge(ind_5, ind_4)
    graph.AddEdge(ind_1, ind_1)

    way = graph.DepthFirstSearch(ind_1, ind_6)
    assert way == []

    graph.AddEdge(ind_6, ind_4)
    way = graph.DepthFirstSearch(ind_1, ind_6)
    assert way == [new_vertex_1, new_vertex_2, new_vertex_4, new_vertex_6]
