class EdgeData:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

    def __repr__(self):
        return f'Edge(src: {self.src}, dest: {self.dest}, weight: {self.weight})'

    def set_weight(self, weight: float) -> None:
        self.weight = weight
