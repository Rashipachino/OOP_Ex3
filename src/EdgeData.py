class EdgeData:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight
        self.tag = 0

    def __repr__(self):
        return f'Edge(src: {self.src}, dest: {self.dest}, weight: {self.weight})'

    def set_weight(self, weight: float) -> None:
        self.weight = weight

    def set_tag(self, tag: int) -> None:
        self.tag = tag
