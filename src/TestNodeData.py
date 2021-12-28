from unittest import TestCase

from src.EdgeData import EdgeData
from src.NodeData import NodeData


class TestNodeData(TestCase):
    global n, v, r
    n = NodeData(5)
    v = NodeData(7)
    r = NodeData(2)

    def test_set_weight(self):
        n.set_weight(1.5)
        self.assertEquals(n.weight, 1.5)

    def test_add_in_edge(self):
        e = EdgeData(5, 7, 1)
        n.add_in_edge(e)
        self.assertEquals(len(n.inEdges), 1)

    def test_add_out_edge(self):
        e = EdgeData(7, 5, 1)
        n.add_out_edge(e)
        self.assertEquals(len(n.outEdges), 1)

    def test_remove_in_edge(self):
        e = EdgeData(2, 7, 1.1)
        v.add_in_edge(e)
        v.remove_in_edge(2)
        self.assertEquals(v.inEdges, {})

    def test_remove_out_edge(self):
        e = EdgeData(2, 7, 1.1)
        r.add_out_edge(e)
        r.remove_out_edge(7)
        self.assertEquals(r.outEdges, {})
