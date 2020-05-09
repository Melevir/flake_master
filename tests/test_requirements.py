from flake_master.utils.requirements import merge_requirements_data


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
