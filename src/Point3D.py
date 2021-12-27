class Point3D:

    def __init__(self, pos: tuple):
        self.x, self.y, self.z = pos

    def get_pos2D(self):
        return self.x, self.y