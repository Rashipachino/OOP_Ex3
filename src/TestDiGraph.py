from unittest import TestCase

from src.DiGraph import DiGraph
from src.NodeData import NodeData


class TestDiGraph(TestCase):
    global g
    g = DiGraph()
    for n in range(10):
        g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 5)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 4, 2.1)
        g.add_edge(4, 2, .5)

    def test_v_size(self):
        self.assertEquals(g.v_size(), 10)

    def test_e_size(self):
        self.assertEquals(g.e_size(), 8)

    def test_get_mc(self):
        mc1 = g.get_mc()
        g.add_edge(4, 3, 1.1)
        mc2 = g.get_mc()
        g.remove_edge(4, 3)
        mc3 = g.get_mc()
        g.add_node(19)
        mc4 = g.get_mc()
        g.remove_node(19)
        mc5 = g.get_mc()
        self.assertNotEquals(mc1, mc2)
        self.assertNotEquals(mc2, mc3)
        self.assertNotEquals(mc3, mc4)
        self.assertNotEquals(mc4, mc5)

    def test_add_edge(self):
        outlen1 = len(g.all_out_edges_of_node(2))
        inlen1 = len(g.all_in_edges_of_node(4))
        g.add_edge(2, 4, 1.3)
        outlen2 = len(g.all_out_edges_of_node(2))
        inlen2 = len(g.all_in_edges_of_node(4))
        self.assertEquals(g.e_size(), 9)
        self.assertNotEquals(outlen1, outlen2)
        self.assertNotEquals(inlen1, inlen2)

    def test_add_node(self):
        self.assertTrue(g.add_node(11))
        self.assertFalse(g.add_node(2))

    def test_remove_node(self):
        len1 = g.v_size()
        edgs = g.e_size()
        ins = len(g.all_in_edges_of_node(5))
        outs = len(g.all_out_edges_of_node(5))
        g.remove_node(5)
        len2 = g.v_size()
        self.assertNotEquals(len1, len2)
        self.assertEquals(g.e_size(), (edgs - ins - outs))

    def test_remove_edge(self):
        len1 = g.e_size()
        g.remove_edge(1, 0)
        len2 = g.e_size()
        self.assertNotEquals(len1, len2)

    def test_get_all_v(self):
        self.assertEquals(len(g.get_all_v()), 10)

    def test_all_in_edges_of_node(self):
        self.assertEquals(len(g.all_in_edges_of_node(3)), 2)

    def test_all_out_edges_of_node(self):
        self.assertEquals(len(g.all_out_edges_of_node(2)), 1)
