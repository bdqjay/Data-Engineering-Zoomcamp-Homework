from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter 


bucket_name = 'mage-zoomcamp-jp'
project_id = 'lateral-raceway-412114'
table_name = 'green_taxi'

root_path = f"{bucket_name}/{table_name}"



@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    Export data (partitioned) to GCS
    """
    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        partition_cols=['lpep_pickup_date'],
        root_path=root_path,
        filesystem=gcs,
    )
