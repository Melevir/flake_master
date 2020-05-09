import json
import os

from click import command, group, argument, Path, echo, pass_context

from flake_master.utils.presets import fetch_preset, apply_preset_to_path


@group()
def cli():
    pass


@command()
@argument('preset_name')
@argument('project_path', type=Path(exists=True))
@pass_context
def setup(ctx, preset_name, project_path):
    """Setup flake8 preset to specified directory."""
    preset_file_name = ctx.obj['preset_file_name']
    preset_file_path = os.path.join(project_path, preset_file_name)
    if os.path.exists(preset_file_path):
        echo(
            f'Preset file ({preset_file_path}) already exists. Looks like flake master '
            f'has already been deployed to {project_path}. May be you mean `upgrade`, not `setup`?',
            err=True,
        )
        exit(1)

    preset = fetch_preset(preset_name_or_url_or_path=preset_name)
    if not preset:
        echo(f'Error fetching preset {preset_name}.', err=True)
        exit(1)

    echo(f'Fetched {preset.name} v. {preset.revision}')
    apply_preset_to_path(preset, project_path, preset_file_name=preset_file_name)
    echo(f'Preset {preset.name} applied.')


@command()
@argument('project_path', type=Path(exists=True))
@pass_context
def upgrade(ctx, project_path):
    """Upgrade already deployed flake8 preset to new version."""
    preset_file_name = ctx.obj['preset_file_name']
    preset_file_path = os.path.join(project_path, preset_file_name)
    if not os.path.exists(preset_file_path):
        echo(
            f'Preset file ({preset_file_path}) not found. Looks like flake master '
            f'was not deployed to {project_path}. May be you mean `setup`, not `upgrade`?',
            err=True,
        )
        exit(1)
    with open(preset_file_path) as file_handler:
        preset_info = json.load(file_handler)
    fresh_preset = fetch_preset(preset_info=preset_info)
    if fresh_preset.revision > preset_info['revision']:
        echo(
            f'Updating preset {preset_info["name"]} from rev. '
            f'{preset_info["revision"]} to {fresh_preset.revision}...',
        )
        apply_preset_to_path(fresh_preset, project_path, preset_file_name=preset_file_name)


cli.add_command(setup)
cli.add_command(upgrade)


def main():
    cli(
        obj={'preset_file_name': '.flake_master'},
    )

if __name__ == '__main__':
    main()
