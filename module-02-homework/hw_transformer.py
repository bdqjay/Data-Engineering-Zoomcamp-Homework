import re
from pandas import DataFrame

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def camel_to_snake(name):
    """
    Convert CamelCase string to snake_case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


@transformer
def execute_transformer_action(data, *args, **kwargs) -> DataFrame:
    """
    Perform required transformations
    """
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data.columns = [camel_to_snake(col) for col in data.columns]
    print(f'Snake cased column names: {data.columns}')
    print(f"Unique vendor ids: {data['vendor_id'].unique()}")
    
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    print(f'Transformed table size: {data.shape}')
    return data
    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert 'vendor_id' in output.columns, "vendor_id should be one of the existing values in the column"
    assert (output['passenger_count'] > 0).all(), "passenger_count should be greater than 0"
    assert (output['trip_distance'] > 0).all(), "trip_distance should be greater than 0"
