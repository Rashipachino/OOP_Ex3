import json
import heapq
from abc import ABC
from typing import List

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
        """
        @return: returns the graph associated with the GraphAlgo
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        loads the graph
        @param file_name: String representing the file path
        @return: returns true if graph was loaded successfully, false otherwise
        """
        try:
            graph = DiGraph()
            with open(file_name, 'r') as file:
                data = json.load(file)
            for n in data["Nodes"]:
                if "pos" in n:
                    pos = n["pos"].split(',')  # split by commas
                    graph.add_node(n["id"], (float(pos[0]), float(pos[1]), float(pos[2])))
                else:
                    graph.add_node(n["id"])
            for e in data["Edges"]:
                graph.add_edge(e["src"], e["dest"], e["w"])
            self.graph = graph
            return True
        except:
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        saves the graph
        @param file_name: String representing the file path
        @return: returns true if the file was saved successfully, false otherwise
        """
        try:
            with open(file_name, 'w') as file:
                json_string = json.dumps(self.graph, cls=GraphEncoder, indent=2)
                file.write(json_string)
            return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
        global node_weight
        if id1 not in self.graph.nodes or id2 not in self.graph.nodes:  # If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
            return float('inf'), []
        if id1 == id2:  # if both ids entered are the same, the path is just the node itself and the cost is zero
            return 0.0, [id1]
        dijkstra = {i: float('inf') for i in self.graph.nodes}  # turning all "weights" to infinity
        dijkstra[id1] = 0  # turns start node's "weight" to 0
        pq = []
        prev = {}
        for n in self.graph.nodes:  # assign all nodes prev = None
            prev[n] = None
            if n != id1:
                heapq.heappush(pq, (float('inf'), n))  # push into heapified list pq
            else:
                heapq.heappush(pq, (0, n))
        while len(pq) != 0:
            node_weight, i = heapq.heappop(pq)
            if dijkstra[i] == float('inf'):  # if popping a node who's weight is infinity, no path exists
                return float('inf'), []
            if i == id2:  # found path
                break
            for dest, w in self.graph.all_out_edges_of_node(i).items():  # all neighbors of i
                if dijkstra[dest] > dijkstra[i] + w:
                    pq.remove((dijkstra[dest], dest))  # removes id from pq
                    dijkstra[dest] = dijkstra[i] + w  # relaxes
                    prev[dest] = i  # updates prev
                    heapq.heappush(pq, (dijkstra[dest], dest))  # push id back into pq with new weight
                    heapq.heapify(pq)
        temp = id2
        short_path = [temp]
        while prev[temp] is not None:  # create list path
            short_path.insert(0, prev[temp])
            temp = prev[temp]
        return node_weight, short_path

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list. Uses helper function closestNodeFinder to
        locate which node in the list is closest to the current node :param node_lst: A list of nodes id's :return: A
        list of the nodes id's in the path, and the overall distance
        """
        if len(node_lst) == 1: # one value in list, return just itself and cost is zero
            return node_lst[0], 0.0
        global path, cost
        min_weight = float('inf')
        min_path = []
        for city in node_lst:
            path = [city]
            cities = node_lst.copy()
            cost = 0.0
            curr = city
            flag = 0
            while True:
                cities.remove(curr)  # remove curr from cities before sending to helper function in order to actually
                # find closest node not including the node itself
                if len(cities) == 1:  # only one left
                    break
                closest_node_path = self._closestNodeFinder(cities, curr)  # returns the shorest path to the closest
                # node and the price is cost to get there
                if closest_node_path[1] == -1:
                    flag = 1
                    break
                path += closest_node_path[0][1:]  # add path except for first value because already added to path
                cost += closest_node_path[1]  # update cost
                curr = closest_node_path[0][-1] # curr now equals what was the next closest node
            if flag == 1:
                continue
            closest_last = self.shortest_path(curr, cities[0])  # finds shortest path from last closest node to last
            # value in cities
            path += closest_last[1][1:]  # adds to path
            cost += closest_last[0]  # updates cost
            if cost < min_weight:  # if this path is really the least costly path, make the path and cost the return values
                min_path = path.copy()
                min_weight = cost
        return min_path, min_weight

    def _closestNodeFinder(self, n_list: List[int], curr_node: int) -> (List[int], float):
        """
        TSP helper function. finds the closest node in the given list to the curr_node
        @param n_list: List of cities to visit
        @param curr_node: starter node
        @return: returns the shortest path from curr_node to closest node in list and the cost to get there
        """
        global curr, node_w
        path_w = 0.0
        dijkstra = {i: float('inf') for i in self.graph.nodes}  # turning all "weights" to infinity
        dijkstra[curr_node] = 0  # turns "weight" of starter node 0
        pq = []
        prev = {}
        for n in self.graph.nodes:
            prev[n] = None
            if n != curr_node:
                heapq.heappush(pq, (float('inf'), n)) # push into heapified list pq
            else:
                heapq.heappush(pq, (0, n))  # push into heapified list pq
        while len(pq) != 0:
            node_w, curr = heapq.heappop(pq)  # pops lowest weighted value in pq
            if dijkstra[curr] == float('inf'):  # if popping a node who's weight is infinity, no path exists
                return [], -1
            if curr in n_list:  #found value in list
                break
            for neighbor, w in self.graph.all_out_edges_of_node(curr).items():  # check neighbors
                if dijkstra[neighbor] > dijkstra[curr] + w:
                    pq.remove((dijkstra[neighbor], neighbor))  # removes id from pq
                    dijkstra[neighbor] = dijkstra[curr] + w  #relaxes
                    prev[neighbor] = curr  # updates prev
                    heapq.heappush(pq, (dijkstra[neighbor], neighbor))  # push id back into pq with new weight
        if len(pq) == 0:  # got to end of list and did not find a closest node
            return [], -1
        temp_node = curr
        path_w += node_w
        dij_path = [temp_node]
        while prev[temp_node] is not None:
            dij_path.insert(0, prev[temp_node])
            temp_node = prev[temp_node]
        return dij_path, node_w

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node. This function uses a helper function
        eccentricity.
        return: The nodes id, min-maximum distance
        """
        min_weight = float('inf')
        center_node = None
        for n in self.graph.nodes:  # go through all nodes in the graph
            ecc_w = self.eccentricity(n, min_weight)  # find out what the eccentricity of the node is
            if ecc_w == float('inf'):  # if the ecc is inf then the graph is not connected and therefore there is no center
                return None, float('inf')
            if ecc_w == -1:  # if the ecc is -1 then the ecc is higher than the current min_weight and stopped early
                continue
            if ecc_w < min_weight:  # if we found a shorter ecc
                min_weight = ecc_w
                center_node = n
        return center_node, min_weight

    def eccentricity(self, node: int, minWeight: float) -> float:
        """
        This is a helper function for centerPoint to find out what the eccentricity from the given node
        :param node: id of node
        :param minWeight: the minWeight that has been found so far
        :return: the eccentricity of the graph from the given node
        """
        dijkstra = {i: float('inf') for i in self.graph.nodes}  # to hold all of the weights between each node to the given node
        dijkstra[node] = 0  # weight is 0 to itself
        pq = []  # priority queue
        for n in self.graph.nodes:  # to fill up the priority queue
            if n != node:
                heapq.heappush(pq, (float('inf'), n))
            else:
                heapq.heappush(pq, (0, n))
        while len(pq) != 0:  # go until the priority queue is not empty
            curr_w, curr_n = heapq.heappop(pq)  # take out the smallest distance from the priority queue
            if curr_w == float('inf'):  # if the weight of the node is inf then the graph is not connected
                return float('inf')
            if len(pq) == 0:  # if the pq is now empty
                return curr_w  # this node has the highest weight from the given node and there is the eccentricity
            if curr_w > minWeight:  # if the weight of the node is higher than the given minWeight then this is definitely not the smallest ecc so return -1 flag
                return -1
            for v, w in self.graph.all_out_edges_of_node(curr_n).items():  # go through all of the out edges of the curr_n
                if dijkstra[v] > dijkstra[curr_n] + w:  # if the path through curr_n has a smaller weight then its current weight then relax
                    pq.remove((dijkstra[v], v))
                    dijkstra[v] = dijkstra[curr_n] + w  # relaxing
                    heapq.heappush(pq, (dijkstra[v], v))
                    heapq.heapify(pq)
        return float('inf')

    def plot_graph(self) -> None:
        """
        We used a GUI to represent the graph and perform actions on it
        """
        WindowGUI.game(self)
