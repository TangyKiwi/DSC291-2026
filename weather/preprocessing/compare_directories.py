#!/usr/bin/env python3
"""
Compare s3_downloaded_content and weather_info directories
"""

import os
import pandas as pd

def compare_directories():
    """Compare the two directories and show differences."""
    
    # Get file lists
    s3_dir = "s3_downloaded_content"
    weather_dir = "../weather_info"
    
    print("DIRECTORY COMPARISON")
    print("=" * 60)
    
    # Check if directories exist
    s3_exists = os.path.exists(s3_dir)
    weather_exists = os.path.exists(weather_dir)
    
    print(f"S3 Downloaded Content: {'✓' if s3_exists else '✗'}")
    print(f"Weather Info: {'✓' if weather_exists else '✗'}")
    print()
    
    if not s3_exists or not weather_exists:
        print("One or both directories don't exist!")
        return
    
    # Get file lists
    s3_files = set(os.listdir(s3_dir)) if s3_exists else set()
    weather_files = set(os.listdir(weather_dir)) if weather_exists else set()
    
    # Files only in s3_downloaded_content
    only_in_s3 = s3_files - weather_files
    print(f"Files only in s3_downloaded_content ({len(only_in_s3)}):")
    for file in sorted(only_in_s3):
        print(f"  - {file}")
    print()
    
    # Files only in weather_info
    only_in_weather = weather_files - s3_files
    print(f"Files only in weather_info ({len(only_in_weather)}):")
    for file in sorted(only_in_weather):
        print(f"  - {file}")
    print()
    
    # Common files
    common_files = s3_files & weather_files
    print(f"Common files ({len(common_files)}):")
    for file in sorted(common_files):
        print(f"  - {file}")
    print()
    
    # File size comparison for common files
    print("FILE SIZE COMPARISON (Common Files):")
    print("-" * 50)
    for file in sorted(common_files):
        s3_path = os.path.join(s3_dir, file)
        weather_path = os.path.join(weather_dir, file)
        
        if os.path.isfile(s3_path) and os.path.isfile(weather_path):
            s3_size = os.path.getsize(s3_path)
            weather_size = os.path.getsize(weather_path)
            size_diff = weather_size - s3_size
            status = "✓" if s3_size == weather_size else "⚠"
            print(f"{status} {file:20s} | S3: {s3_size:8,} | Weather: {weather_size:8,} | Diff: {size_diff:+8,}")
        else:
            print(f"? {file:20s} | (not a regular file)")

if __name__ == "__main__":
    compare_directories()
