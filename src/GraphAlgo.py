import json
from abc import ABC
from queue import PriorityQueue
from typing import List
import pygame

from src import GraphInterface, WindowGUI
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphEncoder import GraphEncoder


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
        global node_weight
        if id1 not in self.graph.nodes or id2 not in self.graph.nodes:
            return float('inf'), []
        if id1 == id2:
            return 0.0, [id1]
        dijakstra = {i: float('inf') for i in self.graph.nodes}
        dijakstra[id1] = 0
        pq = PriorityQueue()
        prev = {}
        for n in self.graph.nodes:
            prev[n] = None
            if n != id1:
                pq.put((float('inf'), n))
            else:
                pq.put((0, n))
        while not pq.empty():
            node_weight, i = pq.get()
            if dijakstra[i] == float('inf'):
                return float('inf'), []
            if i == id2:
                break
            for dest, w in self.graph.all_out_edges_of_node(i).items():
                if dijakstra[dest] > dijakstra[i] + w:
                    dijakstra[dest] = dijakstra[i] + w
                    prev[dest] = i
                    pq.put((dijakstra[dest], dest))
        temp = id2
        short_path = [temp]
        while prev[temp] is not None:
            short_path.insert(0, prev[temp])
            temp = prev[temp]
        return node_weight, short_path

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        if len(node_lst) == 1:
            return node_lst[0], 0.0
        global path, cost
        min_weight = float('inf')
        min_path = []
        for city in node_lst:
            path = [city]
            cities = node_lst.copy()
            cost = 0.0
            curr = city
            while True:
                cities.remove(curr)
                if len(cities) == 1:
                    break
                closest_node_path = self._closestNodeFinder(cities, curr)
                if closest_node_path == -1:
                    return [], -1
                path += closest_node_path[0][1:]
                cost += closest_node_path[1]
                curr = closest_node_path[0][-1]
            closest_last = self.shortest_path(curr, cities[0])
            path += closest_last[1][1:]
            cost += closest_last[0]
            if cost < min_weight:
                min_path = path.copy()
                min_weight = cost
        return min_path, min_weight

    def _closestNodeFinder(self, n_list: List[int], curr_node: int) -> (List[int], float):
        global curr, node_w
        path_w = 0.0
        dijkstra = {i: float('inf') for i in self.graph.nodes}
        dijkstra[curr_node] = 0
        pq = PriorityQueue()
        prev = {}
        for n in self.graph.nodes:
            prev[n] = None
            if n != curr_node:
                pq.put((float('inf'), n))
            else:
                pq.put((0, n))
        while not pq.empty():
            node_w, curr = pq.get()
            if curr in n_list:
                break
            for neighbor, w in self.graph.all_out_edges_of_node(curr).items():
                if dijkstra[neighbor] > dijkstra[curr] + w:
                    dijkstra[neighbor] = dijkstra[curr] + w
                    prev[neighbor] = curr
                    pq.put((dijkstra[neighbor], neighbor))
        if pq.empty():
            return -1
        temp_node = curr
        path_w += node_w
        dij_path = [temp_node]
        while prev[temp_node] is not None:
            dij_path.insert(0, prev[temp_node])
            temp_node = prev[temp_node]
        return dij_path, node_w

    def centerPoint(self) -> (int, float):
        pass

    def plot_graph(self) -> None:
        WindowGUI.game(self.graph)

    def transpose(self) -> GraphInterface:
        gt = self.graph.__copy__()
        gt.edges = {}
        for e in self.graph.edges:
            gt.add_edge(e.dest, e.src, e.weight)
        return gt
