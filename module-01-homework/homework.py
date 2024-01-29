#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_names = params.table_names.split(',')
    urls = params.urls.split(',')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    for url in urls:
        if url == "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz":
            csv_name = 'green_tripdata_2019-09.csv.gz'
            table_name = table_names[0]
        elif url == "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv":
            csv_name = 'taxi+_zone_lookup.csv'
            table_name = table_names[1]

        os.system(f"wget {url} -O {csv_name}")

        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

        df = next(df_iter)

        if url == "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz":
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        df.to_sql(name=table_name, con=engine, if_exists='append')

        while True: 
            try:
                t_start = time()
            
                df = next(df_iter)
                if url == "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz":
                    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
                    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
                df.to_sql(name=table_name, con=engine, if_exists='append')

                t_end = time()

                print('Inserted a chunk, took %.3f second' % (t_end - t_start))

            except StopIteration:
                print("Finished ingesting data into the postgres database")
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_names', required=True, help='names of the tables where we will write the results to')
    parser.add_argument('--urls', required=True, help='urls of the csv files')

    args = parser.parse_args()

    main(args)
