import json
import sys
from abc import ABC
from typing import List

from src import GraphInterface
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphEncoder import GraphEncoder
from src.NodeData import NodeData


class GraphAlgo(GraphAlgoInterface, ABC):

    def __init__(self, graph: DiGraph = None) -> None:
        self.graph = graph

    def __copy__(self) -> GraphInterface:
        return self.graph.__copy__()

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        try:
            graph = DiGraph()
            with open(file_name, 'r') as file:
                data = json.load(file)
            for n in data["Nodes"]:
                pos = n["pos"].split(',')
                graph.add_node(n["id"], (float(pos[0]), float(pos[1]), float(pos[2])))
            for e in data["Edges"]:
                graph.add_edge(e["src"], e["dest"], e["w"])
            self.graph = graph
            return True
        except:
            return False

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, 'w') as file:
                json_string = json.dumps(self.graph, cls=GraphEncoder, indent=2)
                file.write(json_string)
            return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if id1 == id2:
            return 0.0, [id1]
        path = []
        src = self.graph.nodes[id1]
        dest = self.graph.nodes[id2]
        node_weights = {}
        for n in self.graph.nodes:
            pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        pass

    def centerPoint(self) -> (int, float):
        pass

    def plot_graph(self) -> None:
        pass

    def transpose(self) -> GraphInterface:
        gt = self.graph.__copy__()
        gt.edges = {}
        for e in self.graph.edges:
            gt.add_edge(e.dest, e.src, e.weight)
        return gt
