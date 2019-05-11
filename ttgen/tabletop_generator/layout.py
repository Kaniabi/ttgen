from dataclasses import dataclass

from ttgen.tabletop_generator.components import _Base


@dataclass
class OpenDeck(_Base):
    count: int = 1
    deck: str = ""

    def generate(self):
        pass

    @property
    def width(self):
        return ((self.count + 1) * 2.0) + (self.count * 0.2)

    @property
    def height(self):
        return 3.2

    @property
    def bottom_margin(self):
        return 0.8
