from abc import ABC

from src.EdgeData import EdgeData
from src.GraphInterface import GraphInterface
from src.NodeData import NodeData


class DiGraph(GraphInterface, ABC):

    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}
        self.mc = 0

    def __copy__(self) -> GraphInterface:
        temp = DiGraph()
        for n in self.nodes:
            temp.add_node(n.id, (n.pos.x, n.pos.y, n.pos.z))
        for e in self.edges:
            temp.add_edge(e.src, e.dest, e.weight)
        return temp

    def __repr__(self) -> str:
        return f'Graph(Nodes: {self.nodes}, Edges: {self.edges})'

    def v_size(self) -> int:
        """
        returns the amount of nodes in the graph
        """
        return len(self.nodes)

    def e_size(self) -> int:
        """
        returns the amount of edges in the graph
        """
        return len(self.edges)

    def get_mc(self) -> int:
        """
        returns the mode counter which increases whenever there is a change to the graph
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        adds an edge to the graph. updates the out edges of the source node id given and the in edges of the dest node
        id given. increments mc by one.
        returns true if the edge to be added does not already exist in the graph and can therefore be successfully added
        returns false otherwise
        """
        if id1 in self.nodes and id2 in self.nodes and (id1, id2) not in self.edges:
            e = EdgeData(id1, id2, weight)
            self.edges[(id1, id2)] = e
            self.nodes[id1].add_out_edge(e)
            self.nodes[id2].add_in_edge(e)
            self.mc += 1
            return True
        return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        adds a node to the graph. increments mc by one.
        returns true if the node does not already exist on the graph and can therefore be successfully added.
        returns false otherwise
        """
        if node_id not in self.nodes:
            self.nodes[node_id] = NodeData(node_id, pos)
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        """
        removes a node from the graph. deletes the node's in and out edges. increments mc by one.
        returns true if the node to be removed is a node in the graph and can therefore be successfully removed.
        returns false otherwise.
        """
        if node_id in self.nodes:
            n = self.nodes.pop(node_id)
            for e in n.outEdges:
                self.nodes[e].remove_in_edge(n.id)
                self.edges.pop((n.id, e))
            for e in n.inEdges:
                self.nodes[e].remove_out_edge(n.id)
                self.edges.pop((e, n.id))
            self.mc += 1
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        removes an edge from the graph. updates the edge's source and dest nodes by deleting said edge from the node's
        in and out edges. increments mc by one.
        returns true if the edge to be removed is an edge in the graph and can therefore be successfully removed.
        returns false otherwise.
        """
        if (node_id1, node_id2) in self.edges:
            self.nodes[node_id1].remove_out_edge(node_id2)
            self.nodes[node_id2].remove_in_edge(node_id1)
            self.edges.pop((node_id1, node_id2))
            self.mc += 1
            return True
        return False

    def get_all_v(self) -> dict:
        """
        returns a dictionary of all the nodes in the graph
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        returns a dictionary of all the in edges of a given node
        """
        return self.nodes[id1].inEdges

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        returns a dictionary of all the out edges of a given node
        """
        return self.nodes[id1].outEdges
