from pathlib import Path
from typing import OrderedDict

import click

from ttgen.tabletop_generator.layout import Layout


@click.group("ttgen")
def main():
    pass


@main.command("compile")
@click.argument("filename")
@click.option("--output-dir")
@click.pass_context
def compile(ctx, filename, output_dir=None):
    """
    Generate tabletop-simulator mods from tabletop-generator specs.
    """
    ttg = TabletopGenerator(filename)
    ttg.compile(output_dir)


class TabletopGenerator:

    def __init__(self, filename):
        import yaml
        from ttgen.tabletop_generator import components, players

        self._source_filename = Path(filename)

        yaml = yaml.load(self._source_filename.open(mode="r"), Loader=yaml.BaseLoader)
        self.name = yaml["name"]

        player_yaml = yaml.get("players", {'__class__': 'TwoPlayers'})
        self.players = self._create_object(
            'players',
            player_yaml,
            class_factory=players
        )

        self.components = OrderedDict()
        for i_component_name, i_component_dict in yaml["components"].items():
            print("*", i_component_name)
            component = self._create_object(
                i_component_name,
                i_component_dict,
                class_factory=components
            )
            self.components[component.get_key()] = component

        layout_yaml = yaml.get("layout", [])
        self.layout = []
        for i_layout_dict in layout_yaml:
            c = Layout.create_layout(i_layout_dict, self.components)
            self.layout.append(c)

        self.apply_layout()

    @classmethod
    def _create_object(cls, name, dd, class_factory):
        class_ = dd.pop("__class__")
        try:
            class_ = getattr(class_factory, class_)
        except AttributeError:
            raise TypeError(f"Invalid component class: {class_}.")
        else:
            return class_.from_dict(dd, name)

    def apply_layout(self):
        """
        Layout is applied on the ttgen components, not the tabletop-simulator.
        """
        table = self.components['table']
        for i_layout in self.layout:
            i_layout.set_position(0.0, 0.0)
            table.annotations.update(i_layout.annotations)

    def compile(self, dest_directory: Path):
        """
        Generate tabletop-simulator from the current ttgen players and
        components.

        :param dest_directory:
        :return:
        """
        from ttgen.tabletop_simulator import TabletopSimulator

        click.echo("Compiling...")

        ttsim = TabletopSimulator()
        ttsim.SaveName = self.name
        ttsim.GameMode = self.name

        # Ttgen components are added into tabletop-simulator ObjectStates.
        for i_component in self.components.values():
            ttsim.ObjectStates += i_component.generate(
                dest_directory=self._source_filename.parent.absolute()
            )

        # Ttgen players generate the tabletop-simulator HandTransforms
        ttsim.Hands.HandTransforms += self.players.generate()

        # Save the generated file on destination directory.
        ttsim.save(Path(dest_directory) / f"{self.name}.json")

        # DEBUG: Saves the generated file locally for debugging.
        ttsim.save(self._source_filename.parent / f"{self.name}.json")


if __name__ == "__main__":
    main()
