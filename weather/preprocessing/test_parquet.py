#!/usr/bin/env python3
"""
Test script to check parquet file structure
"""

import dask.dataframe as dd
import pandas as pd
import os

def test_parquet_files():
    """Test reading parquet files and identify any issues."""
    
    # Check which parquet files exist
    weather_info_dir = '../weather_info'
    stations_file = os.path.join(weather_info_dir, 'stations_dask.parquet')
    inventory_file = os.path.join(weather_info_dir, 'inventory_dask.parquet')
    
    print("Available parquet files:")
    print(f"Stations: {os.path.exists(stations_file)}")
    print(f"Inventory: {os.path.exists(inventory_file)}")
    
    # Test stations file
    if os.path.exists(stations_file):
        print(f"\n=== TESTING STATIONS PARQUET ===")
        try:
            stations_df = dd.read_parquet(stations_file)
            print(f"✓ Successfully loaded stations parquet")
            print(f"Partitions: {stations_df.npartitions}")
            print(f"Columns: {list(stations_df.columns)}")
            
            # Test basic operations
            sample = stations_df.head(3).compute()
            print(f"✓ Sample data loaded: {len(sample)} rows")
            print(sample)
            
        except Exception as e:
            print(f"✗ Error loading stations: {e}")
    
    # Test inventory file
    if os.path.exists(inventory_file):
        print(f"\n=== TESTING INVENTORY PARQUET ===")
        try:
            inventory_df = dd.read_parquet(inventory_file)
            print(f"✓ Successfully loaded inventory parquet")
            print(f"Partitions: {inventory_df.npartitions}")
            print(f"Columns: {list(inventory_df.columns)}")
            
            # Test basic operations
            sample = inventory_df.head(3).compute()
            print(f"✓ Sample data loaded: {len(sample)} rows")
            print(sample)
            
        except Exception as e:
            print(f"✗ Error loading inventory: {e}")

if __name__ == "__main__":
    test_parquet_files()
