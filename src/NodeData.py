from src.EdgeData import EdgeData
from src.Point3D import Point3D


class NodeData:

    def __init__(self, node_id: int, pos: tuple) -> None:
        self.id = node_id
        self.pos = Point3D(pos)
        self.weight = 0
        self.tag = 0
        self.inEdges = {}
        self.outEdges = {}
        self.prev = None

    def __copy__(self):
        return NodeData(self.id, (self.pos.x, self.pos.y, self.pos.z))

    def set_pos(self, pos: tuple) -> None:
        self.pos = Point3D(pos)

    def set_weight(self, weight: float) -> None:
        self.weight = weight

    def set_tag(self, tag: int) -> None:
        self.tag = tag

    def set_prev(self, prev: int) -> None:
        self.prev = prev

    def add_in_edge(self, e: EdgeData) -> None:
        self.inEdges[e.src] = e.weight

    def add_out_edge(self, e: EdgeData) -> None:
        self.outEdges[e.dest] = e.weight

    def remove_in_edge(self, dest: int) -> EdgeData:
        return self.inEdges.pop(dest)

    def remove_out_edge(self, src: int) -> EdgeData:
        return self.inEdges.pop(src)
