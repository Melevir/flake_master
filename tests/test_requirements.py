import deal
from hypothesis.strategies import lists, one_of

from flake_master.utils.requirements import merge_requirements_data
from flake_master.utils.testing_strategies import requirement


test_merge_requirements_data = deal.cases(
    merge_requirements_data,
    kwargs={
        'raw_old_requirements': lists(
            one_of(
                requirement(with_version=True, with_comment=True),
                requirement(with_version=True, with_comment=False),
                requirement(with_version=False, with_comment=True),
                requirement(with_version=False, with_comment=False),
                requirement(only_comment=True),
            ),
        ),
    }
)


def test_merge_requirements_data_succes_case():
    actual_result = merge_requirements_data(
        raw_old_requirements=['foo', 'bar==1.2', 'baz>=2.0'],
        flake8_plugins=[('bar', '2.1'), ('bax', '5')],
    )
    assert actual_result == '''foo
bar==2.1
baz>=2.0
bax==5
'''
