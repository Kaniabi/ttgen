from pathlib import Path
from typing import OrderedDict

import click


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
    ttg.compile(
        output_dir
    )


class TabletopGenerator:

    def __init__(self, filename):
        import yaml
        from ttgen.tabletop_generator import components, layout

        self._source_filename = Path(filename)

        yaml = yaml.load(self._source_filename.open(mode="r"), Loader=yaml.BaseLoader)
        self.name = yaml["name"]

        self.components = OrderedDict()
        for i_component_name, i_component_dict in yaml["components"].items():
            print("*", i_component_name)
            component_class = i_component_dict.pop("__class__")
            try:
                class_ = getattr(components, component_class)
            except AttributeError:
                raise TypeError(f"Invalid component class: {component_class}.")
            else:
                c = class_.schema().load(i_component_dict)
            self.components[i_component_name] = c

        self.layout = []
        for i_layout in yaml["layout"]:
            layout_class = i_layout.pop("__class__")
            try:
                class_ = getattr(layout, layout_class)
            except AttributeError:
                raise TypeError(f"Invalid layout class: {layout_class}.")
            else:
                c = class_.schema().load(i_layout)
            self.layout.append(c)

    def compile(self, dest_directory: Path):
        from ttgen.tabletop_simulator import TabletopSimulator

        click.echo("Compiling...")

        ttsim = TabletopSimulator()
        ttsim.SaveName = self.name
        ttsim.GameMode = self.name
        ttsim.generate_components(self.components, source_dir=self._source_filename.parent)
        self.calculate_layout(ttsim)
        ttsim.save(self._source_filename.parent / f"{self.name}.json")
        ttsim.save(Path(dest_directory) / f"{self.name}.json")

    def calculate_layout(self, layout):
        pass
        # width = sum(i.width for i in layout)
        # height = sum(i.height for i in layout)


if __name__ == "__main__":
    main()
