from typing import List, Tuple, Optional

import deal
from requirements.requirement import Requirement


@deal.pure
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
        requirement_str = old_requirement.strip()
        if requirement_str.startswith('#'):
            continue
        try:
            parsed_requirement = Requirement.parse(requirement_str) if requirement_str else None
        except ValueError:
            # happens on weird chars in requirements, like `parsed_requirement = 'A  # \x850'`
            continue
        if parsed_requirement and parsed_requirement.name == package_name:
            match_line_num = old_requirement_num
    return match_line_num
