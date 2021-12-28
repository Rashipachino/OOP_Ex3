from src.EdgeData import EdgeData
from src.Point3D import Point3D


class NodeData:

    def __init__(self, node_id: int, pos: tuple = None) -> None:
        self.id = node_id
        if pos is not None:
            self.pos = Point3D(pos)
        else:
            self.pos = None
        self.weight = 0
        self.inEdges = {}
        self.outEdges = {}

    def __copy__(self):
        return NodeData(self.id, (self.pos.x, self.pos.y, self.pos.z))

    def __repr__(self):
        return f'{self.id}: |edges_out| {len(self.outEdges)} |edges in| {len(self.inEdges)}'

    def set_pos(self, pos: tuple) -> None:
        self.pos = Point3D(pos)

    def set_weight(self, weight: float) -> None:
        self.weight = weight

    def add_in_edge(self, e: EdgeData) -> None:
        self.inEdges[e.src] = e.weight

    def add_out_edge(self, e: EdgeData) -> None:
        self.outEdges[e.dest] = e.weight

    def remove_in_edge(self, src: int) -> EdgeData:
        return self.inEdges.pop(src)

    def remove_out_edge(self, dest: int) -> EdgeData:
        return self.outEdges.pop(dest)
