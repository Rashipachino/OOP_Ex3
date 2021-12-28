from unittest import TestCase

from src.Point3D import Point3D


class TestPoint3D(TestCase):
    global p
    p = Point3D((32, 35, 0))
    def test_get_pos2D(self):
        self.assertEquals(p.get_pos2D(),  (32, 35))
