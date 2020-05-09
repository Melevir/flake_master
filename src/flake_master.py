from click import command, group, argument, Path, echo

from utils.presets import fetch_preset, apply_preset_to_path


@group()
def cli():
    pass


@command()
@argument('preset_name')
@argument('project_path', type=Path(exists=True))
def setup(preset_name, project_path):
    """Setup flake8 preset to specified directory."""
    preset = fetch_preset(preset_name)
    if not preset:
        echo(f'Error fetching preset {preset_name}.', err=True)
        exit(1)
    echo(f'Fetched {preset.name} v. {preset.revision}')
    apply_preset_to_path(preset, project_path)
    echo(f'Preset {preset.name} applied.')


@command()
def upgrade(project_path):
    """Upgrade already deployed flake8 preset to new version."""
    pass


cli.add_command(setup)
cli.add_command(upgrade)


if __name__ == '__main__':
    cli()
