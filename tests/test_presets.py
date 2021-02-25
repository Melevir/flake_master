import deal

from flake_master.utils.presets import (
    extract_preset_file_path, extract_preset_url, extract_preset_credentials,
)


test_extract_preset_file_path = deal.cases(extract_preset_file_path)
test_extract_preset_url = deal.cases(extract_preset_url)
test_extract_preset_credentials = deal.cases(extract_preset_credentials)
