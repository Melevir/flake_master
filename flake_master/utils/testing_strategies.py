import string

from hypothesis.strategies import text, integers


def requirement(only_comment=False, with_version=True, with_comment=True):
    if only_comment:
        return text().map(lambda r: f'# {r}')

    package_name = text(string.ascii_letters, min_size=1)
    if with_comment and not with_version:
        return package_name.flatmap(
            lambda p: text(min_size=1).map(lambda c: f'{p}  # {c}'),
        )

    if with_version:
        return package_name.flatmap(
            lambda t: integers().flatmap(
                lambda i: text(min_size=1).map(
                    lambda c: f'{t} == {i}  # {c}' if with_comment else f'{t}=={i}',
                ),
            ),
        )
    else:
        return package_name
