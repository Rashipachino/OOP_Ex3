from json import JSONEncoder

from src.DiGraph import DiGraph


class GraphEncoder(JSONEncoder):
    def default(self, graph: DiGraph) -> dict:
        if isinstance(graph, DiGraph):
            nodes = []
            for n in graph.nodes.values():
                if n.pos is not None:
                    nodes.append({"pos": "{},{},{}".format(n.pos.x, n.pos.y, n.pos.z), "id": n.id})
                else:
                    nodes.append({"id": n.id})
            edges = []
            for e in graph.edges.values():
                edges.append({"src": e.src, "w": e.weight, "dest": e.dest})
            return {"Edges": edges, "Nodes": nodes}
