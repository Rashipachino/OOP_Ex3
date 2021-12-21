class EdgeData:

    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight
        self.tag = 0

    def set_weight(self, weight: float) -> None:
        self.weight = weight

    def set_tag(self, tag: int) -> None:
        self.tag = tag
