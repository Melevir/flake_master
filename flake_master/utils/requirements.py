from typing import List, Tuple, Optional

from requirements.requirement import Requirement


def merge_requirements_data(
    raw_old_requirements: List[str],
    flake8_plugins: List[Tuple[str, str]],
) -> str:
    new_packages_to_add = []
    for package_name, package_version in flake8_plugins:
        match_line_num = find_requirement_in_list(package_name, raw_old_requirements)
        if match_line_num is not None:
            raw_old_requirements.pop(match_line_num)
            raw_old_requirements.insert(match_line_num, f'{package_name}=={package_version}')
        else:
            new_packages_to_add.append((package_name, package_version))
    return '\n'.join(raw_old_requirements + [f'{p}=={v}' for (p, v) in new_packages_to_add]) + '\n'


def find_requirement_in_list(package_name: str, raw_old_requirements: List[str]) -> Optional[int]:
    match_line_num = None
    for old_requirement_num, old_requirement in enumerate(raw_old_requirements):
        parsed_requirement = Requirement.parse(old_requirement) if old_requirement.strip() else None
        if parsed_requirement and parsed_requirement.name == package_name:
            match_line_num = old_requirement_num
    return match_line_num
