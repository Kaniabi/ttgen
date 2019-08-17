from dataclasses import dataclass

from ttgen.tabletop_simulator import TabletopHandTransform, TabletopTransform
from .components import _Base

@dataclass
class TwoPlayers(_Base):

    def generate(self):
        table_x = 18.0
        table_z = 18.0
        box_x = 12.0
        box_y = 6.0
        box_z = 6.0

        result = [
            TabletopHandTransform(
                Color='Red',
                Transform=TabletopTransform(
                    posX= - (table_x - (box_x // 2)),
                    posY=3.24,
                    posZ= - (table_z - (box_z // 2)),
                    rotY=0.0,
                    scaleX=box_x,
                    scaleY=box_y,
                    scaleZ=box_z,
                )
            ),
            TabletopHandTransform(
                Color='Blue',
                Transform=TabletopTransform(
                    posX= + (table_x - (box_x // 2)),
                    posY=3.24,
                    posZ= - (table_z - (box_z // 2)),
                    rotY=0.0,
                    scaleX=box_x,
                    scaleY=box_y,
                    scaleZ=box_z,
                )
            )
        ]
        return result
