from dataclasses import dataclass

from sympy import Polygon, Point2D

from ttgen.dataclass_ import RgbType


class _BaseAnnotation:

    def configure_surface(self, ttgen_table, ttsim_table):
        raise NotImplementedError


@dataclass
class SnapPoint(_BaseAnnotation):

    position: Point2D = Point2D()

    def configure_surface(self, ttgen_table, ttsim_table):
         from ttgen.tabletop_simulator import AttachedSnapPoint
         p = AttachedSnapPoint.from_dict(
             Position=dict(
                 x=float(self.position.x),
                 y=ttgen_table.surface_y,
                 z=float(self.position.y)
             )
         )
         ttsim_table.AttachedSnapPoints.append(p)


@dataclass
class Box(_BaseAnnotation):

    polygon: Polygon = Polygon((0, 0), (1, 0), (1, 1), (0, 1))
    color: RgbType = RgbType()
    thickness: float = 0.02

    def configure_surface(self, ttgen_table, ttsim_table):
        from ttgen.tabletop_simulator import AttachedVectorLine
        points3 = [
            dict(
                x=float(self.polygon.vertices[i].x),
                y=ttgen_table.surface_y,
                z=float(self.polygon.vertices[i].y),
            )
            for i in range(4)
        ]
        a = AttachedVectorLine.from_dict(
            points3=points3,
            color=self.color,
            thickness=self.thickness,
        )
        ttsim_table.AttachedVectorLines.append(a)


class Annotations:

    def __init__(self):
        self._annotations = []

    def __iter__(self):
        return self._annotations.__iter__()

    def update(self, other):
        self._annotations += other._annotations

    def add_snap_point(self, x, y):
        a = SnapPoint(
            position=Point2D(x, y)
        )
        self._annotations.append(a)

    def add_box(self, x, y, w, h, color):
        a = Box(
            polygon=Polygon((x, y), (x + w, y), (x + w, y + h), (x, y + h)),
            color=color,
        )
        self._annotations.append(a)
