#!/usr/bin/env python3
"""
Download S3 Content Script

This script downloads content from the NOAA GHCN S3 bucket, excluding:
- csv directory
- csv.gz files  
- parquet directory

Usage:
    python download_s3_content.py --output_dir ./downloaded_data
"""

import os
import argparse
import s3fs
from datetime import datetime
import time

def setup_output_directory(output_dir):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    return output_dir

def should_download_file(file_path):
    """
    Determine if a file should be downloaded based on exclusion rules.
    
    Args:
        file_path: S3 file path
        
    Returns:
        bool: True if file should be downloaded, False otherwise
    """
    # Exclude csv directory
    if '/csv/' in file_path:
        return False
    
    # Exclude csv.gz files
    if file_path.endswith('.csv.gz'):
        return False
    
    # Exclude parquet directory
    if '/parquet/' in file_path:
        return False
    
    return True

def download_s3_content(bucket_name, output_dir, max_files=None):
    """
    Download content from S3 bucket with exclusions.
    
    Args:
        bucket_name: S3 bucket name
        output_dir: Local output directory
        max_files: Maximum number of files to download (None for all)
    """
    print(f"Connecting to S3 bucket: {bucket_name}")
    s3 = s3fs.S3FileSystem(anon=True)
    
    print("Scanning S3 bucket for files to download...")
    
    # Get all files recursively
    all_files = s3.find(bucket_name)
    
    # Filter files based on exclusion rules
    files_to_download = [f for f in all_files if should_download_file(f)]
    
    print(f"Found {len(all_files)} total files in bucket")
    print(f"Will download {len(files_to_download)} files (after exclusions)")
    
    if max_files:
        files_to_download = files_to_download[:max_files]
        print(f"Limited to {max_files} files for this run")
    
    # Download files
    downloaded_count = 0
    skipped_count = 0
    error_count = 0
    
    start_time = time.time()
    
    for i, s3_path in enumerate(files_to_download, 1):
        try:
            # Create relative path from bucket
            relative_path = s3_path.replace(f"{bucket_name}/", "")
            local_path = os.path.join(output_dir, relative_path)
            
            # Create local directory if needed
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir)
            
            # Download file
            print(f"[{i:3d}/{len(files_to_download)}] Downloading: {relative_path}")
            s3.download(s3_path, local_path)
            downloaded_count += 1
            
        except Exception as e:
            print(f"  ❌ Error downloading {s3_path}: {e}")
            error_count += 1
            continue
    
    end_time = time.time()
    download_time = end_time - start_time
    
    # Summary
    print(f"\n{'='*60}")
    print("DOWNLOAD SUMMARY")
    print(f"{'='*60}")
    print(f"Files downloaded: {downloaded_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total time: {download_time:.1f} seconds")
    print(f"Average time per file: {download_time/downloaded_count:.2f} seconds" if downloaded_count > 0 else "No files downloaded")
    print(f"Output directory: {output_dir}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Download S3 content with exclusions')
    parser.add_argument('--output_dir', type=str, default='./downloaded_s3_content',
                       help='Output directory for downloaded files (default: ./downloaded_s3_content)')
    parser.add_argument('--max_files', type=int, default=None,
                       help='Maximum number of files to download (default: all)')
    parser.add_argument('--bucket', type=str, default='noaa-ghcn-pds',
                       help='S3 bucket name (default: noaa-ghcn-pds)')
    
    args = parser.parse_args()
    
    print("S3 Content Downloader")
    print("=" * 40)
    print(f"Bucket: {args.bucket}")
    print(f"Output directory: {args.output_dir}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup output directory
    output_dir = setup_output_directory(args.output_dir)
    
    # Download content
    download_s3_content(args.bucket, output_dir, args.max_files)
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
