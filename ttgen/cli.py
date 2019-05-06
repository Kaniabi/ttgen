from pathlib import Path
import click


@click.group('ttgen')
def main():
    pass


@main.command('compile')
@click.argument('filename')
@click.pass_context
def compile(ctx, filename):
    """
    Generate tabletop-simulator mods from tabletop-generator specs.
    """
    ttg = TabletopGenerator(filename)
    ttg.compile('/c/Users/kania/Documents/my games/Tabletop Simulator/Mods/Workshop/Testing')


class TabletopGenerator:

    def __init__(self, filename):
        import yaml

        self._source_filename = Path(filename)

        yaml = yaml.load(self._source_filename.open(mode='r'))

        for i_component in yaml['components']:
            print('*', i_component)

    def compile(self, dest_directory):
        click.echo("Compiling...")
        dest_directory = Path(dest_directory)
        template = Path('ttgen-template.json')
        target = Path(dest_directory / 'Anachrony.json')
        target.write_bytes(template.read_bytes())


if __name__ == '__main__':
    main()
