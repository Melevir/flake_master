from flake_master.utils.preset_fetchers import parse_preset_from_str_config


def test_parse_preset_from_str_config(preset_file_content, preset_file_path, preset_url):
    preset = parse_preset_from_str_config(
        preset_file_content,
        preset_file_path,
        preset_url,
    )
    assert preset.config_url == preset_url
    assert preset.filepath == preset_file_path
    assert preset.revision == '6'
    assert len(preset.flake8_config) == 1
    assert len(preset.flake8_plugins) == 1
