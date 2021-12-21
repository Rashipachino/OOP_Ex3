import json
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

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        graph = DiGraph()
        with open(file_name, 'r') as file:
            data = json.load(file)
        for n in data["Nodes"]:
            pos = n["pos"].split(',')
            graph.add_node(n["id"], (float(pos[0]), float(pos[1]), float(pos[2])))
        for e in data["Edges"]:
            graph.add_edge(e["src"], e["dest"], e["w"])
        self.graph = graph

    def save_to_json(self, file_name: str) -> bool:
        with open(file_name, 'w') as file:
            json_string = json.dumps(self.graph, cls=GraphEncoder, indent=2)
            file.write(json_string)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        super().TSP(node_lst)

    def centerPoint(self) -> (int, float):
        super().centerPoint()

    def plot_graph(self) -> None:
        pass
