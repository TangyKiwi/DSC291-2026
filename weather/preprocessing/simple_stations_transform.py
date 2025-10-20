#!/usr/bin/env python3
import dask.dataframe as dd
import pandas as pd

# Read the stations file
print("Reading GHCN stations file...")
df = pd.read_fwf(
    's3_downloaded_content/ghcnd-stations.txt',
    colspecs=[(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71), (72, 75), (76, 79), (80, 85)],
    names=['station_id', 'latitude', 'longitude', 'elevation', 'state', 'name', 'gsn_flag', 'hcn_crn_flag', 'wmo_id'],
    na_values=['', ' ']
)

print(f"Loaded {len(df)} stations")
print("Sample data:")
print(df.head())

# Convert to Dask DataFrame
dask_df = dd.from_pandas(df, npartitions=4)
print(f"\nConverted to Dask DataFrame with {dask_df.npartitions} partitions")
print("Dask DataFrame info:")
print(dask_df.head())
