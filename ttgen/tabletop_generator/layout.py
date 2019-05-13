from dataclasses import dataclass, field
from typing import List

from ttgen.dataclass_ import RgbType
from ttgen.tabletop_generator.components import _Base


@dataclass
class Layout(_Base):

    items: List = field(default_factory=list)

    def set_position(self, x, y):
        raise NotImplementedError()

    def initialize(self, components):
        pass

    @classmethod
    def create_layout(cls, d: dict, components: dict) -> object:
        layout_class = d.pop("__class__")
        try:
            class_ = globals()[layout_class]
        except KeyError:
            raise TypeError(f"Invalid layout class: {layout_class}.")

        result = class_.schema().load(d)
        result.items = [cls.create_layout(i, components) for i in result.items]
        result.initialize(components)
        return result


@dataclass
class OpenDeck(Layout):
    count: int = 1
    margin: float = 0.4

    # References
    table: str = ""
    deck: str = ""

    # TODO: This is a deck-component property.
    deck_width = 2.2

    def set_position(self, x, y):
        from ttgen.dataclass_ import PosType

        cur_x = x - (self.width / 2.0) + (self.deck_width / 2.0)
        self.deck.position = PosType(cur_x, y)

        for _ in range(self.count + 1):
            self.table.add_snap_point(cur_x, y)
            cur_x += (self.deck_width + self.margin)

        self.table.add_box(
            x=x - (self.width / 2.0),
            y=y - (self.height / 2.0),
            w=self.width,
            h=self.height,
            color=RgbType(1.0, 0.85, 0.95),
        )

    def initialize(self, components):
        self.deck = components[f'deck:{self.deck}']
        self.table = components['table']

    @property
    def width(self):
        result = self.deck_width * (self.count + 1)
        result += self.margin * self.count
        return result

    @property
    def height(self):
        return 3.2



@dataclass
class VerticalBox(Layout):

    margin: float = 0.8

    def set_position(self, x, y):
        height = sum(i.height for i in self.items)
        height += (len(self.items) - 1) * self.margin

        cur_y = y - (height / 2.0)
        for i, i_item in enumerate(self.items):
            h = i_item.height
            i_item.set_position(x, cur_y + (h / 2.0))
            cur_y += h + self.margin


@dataclass
class HorizontalBox(Layout):

    margin: float = 0.4

    def set_position(self, x, y):
        width = sum(i.width for i in self.items)
        width += (len(self.items) - 1) * self.margin

        cur_x = x - (width / 2.0)
        for i, i_item in enumerate(self.items):
            w = i_item.width
            i_item.set_position(cur_x + (w / 2.0), y)
            cur_x += w + self.margin
