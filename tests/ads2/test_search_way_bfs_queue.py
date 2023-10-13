from lessons.ads2.search_way_bfs_queue import SimpleGraph


def test_search_way():
    graph = SimpleGraph(12)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)
    new_vertex_4 = graph.AddVertex(4)
    new_vertex_5 = graph.AddVertex(5)
    new_vertex_6 = graph.AddVertex(6)
    new_vertex_7 = graph.AddVertex(7)
    new_vertex_8 = graph.AddVertex(8)
    new_vertex_9 = graph.AddVertex(9)
    new_vertex_10 = graph.AddVertex(10)
    new_vertex_11 = graph.AddVertex(11)
    new_vertex_12 = graph.AddVertex(12)

    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)
    ind_3 = graph.vertex.index(new_vertex_3)
    ind_4 = graph.vertex.index(new_vertex_4)
    ind_5 = graph.vertex.index(new_vertex_5)
    ind_6 = graph.vertex.index(new_vertex_6)
    ind_7 = graph.vertex.index(new_vertex_7)
    ind_8 = graph.vertex.index(new_vertex_8)
    ind_9 = graph.vertex.index(new_vertex_9)
    ind_10 = graph.vertex.index(new_vertex_10)
    ind_11 = graph.vertex.index(new_vertex_11)
    ind_12 = graph.vertex.index(new_vertex_12)

    graph.AddEdge(ind_1, ind_2)
    graph.AddEdge(ind_1, ind_3)
    graph.AddEdge(ind_1, ind_4)
    graph.AddEdge(ind_2, ind_5)
    graph.AddEdge(ind_2, ind_6)
    graph.AddEdge(ind_3, ind_7)
    graph.AddEdge(ind_4, ind_8)
    graph.AddEdge(ind_4, ind_9)
    graph.AddEdge(ind_4, ind_11)
    graph.AddEdge(ind_8, ind_9)
    graph.AddEdge(ind_8, ind_10)
    graph.AddEdge(ind_1, ind_1)

    way = graph.BreadthFirstSearch(ind_1, ind_9)
    assert way == [new_vertex_1, new_vertex_4, new_vertex_9]

    assert graph.BreadthFirstSearch(ind_1, ind_12) == []

    assert graph.BreadthFirstSearch(ind_1, ind_2) == [new_vertex_1, new_vertex_2]

def test_way_2():
    graph = SimpleGraph(4)
    new_vertex_1 = graph.AddVertex(1)
    new_vertex_2 = graph.AddVertex(2)
    new_vertex_3 = graph.AddVertex(3)
    new_vertex_4 = graph.AddVertex(4)

    ind_1 = graph.vertex.index(new_vertex_1)
    ind_2 = graph.vertex.index(new_vertex_2)
    ind_3 = graph.vertex.index(new_vertex_3)
    ind_4 = graph.vertex.index(new_vertex_4)
    graph.AddEdge(ind_1, ind_2)
    way = graph.BreadthFirstSearch(ind_2, ind_1)
    assert way == [new_vertex_2, new_vertex_1]