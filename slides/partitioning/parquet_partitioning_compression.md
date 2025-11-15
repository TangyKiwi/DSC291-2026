# Parquet, Partitioning, and Compression with Dask

**Title**: Parquet, Partitioning, and Compression with Dask  
**Subtitle**: Optimizing Data Storage for Scalable Analytics  
**Author**: CSE255 - Scalable Data Analysis

---

## Slide 1: Title Page

---

## Slide 2: Why Parquet?

**Traditional Formats:**
- CSV: Text-based, no schema
- JSON: Nested, but verbose
- Pickle: Python-only, not cross-platform

**Parquet Advantages:**
- **Columnar** storage
- **Schema** embedded
- **Compression** built-in
- **Cross-platform** (Java, Python, R, Spark, etc.)
- Efficient **projection** (read only needed columns)

---

## Slide 3: Columnar vs Row-Oriented Storage

**Row-Oriented (CSV):**
| Format | Year | Temp | Station |
|--------|------|------|---------|
| Row 1  | 1950 | 15.2 | US001   |
| Row 2  | 1950 | 18.5 | US002   |
| Row 3  | 1950 | 12.8 | US003   |

**Columnar (Parquet):**
- **Year**: 1950, 1950, 1950...
- **Temp**: 15.2, 18.5, 12.8...

Only read columns you need → Faster queries

---

## Slide 4: Basic Parquet with Dask

```python
import dask.dataframe as dd

# Read multiple Parquet files
df = dd.read_parquet('s3://bucket/data/*.parquet')

# Convert DataFrame to Parquet
df.to_parquet(
    'output/',
    engine='pyarrow',
    compression='snappy'
)
```

**Key Features:**
- Automatic schema inference
- Partitioned by default (one file per partition)
- Compression reduces size 3-10x vs CSV

---

## Slide 5: Parquet Schema

**Schema = Data Type + Metadata**

| Column     | Type      | Metadata           |
|------------|-----------|--------------------|
| year       | int32     | nullable           |
| temp       | float64   | nullable           |
| station_id | string    | categorical        |
| date       | timestamp | timezone=UTC       |

**Benefits:**
- No guessing data types when reading
- Automatic validation
- Categorical encoding for strings

---

## Slide 6: Partitioning Strategy

```python
# Partition by single column
df.to_parquet(
    'output/',
    partition_on=['year']  # Creates: year=2020/, year=2021/
)

# Partition by multiple columns
df.to_parquet(
    'output/',
    partition_on=['year', 'country']  # year=2020/country=US/
)

# Custom partitioning with repartition
df = df.repartition(npartitions=20)
df.to_parquet('output/')
```

---

## Slide 7: Partitioning Benefits

**Time-based Partitioning:**
- `year=2020/day=01/`
- Filter before reading
- Skip entire directories
- Fast time-range queries

**Size-based:**
- Target: 128MB per file
- Balanced parallel processing
- Reasonable memory usage

**Strategy Examples:**

**Weather Data:**
- `year=YYYY/month=MM/`
- Read: Last 3 months
- Read: Single year for yearly analysis

**Taxi Data:**
- `year=YYYY/month=MM/`
- Filter: Peak season only

---

## Slide 8: Reading Partitioned Data

```python
# Read entire dataset
df = dd.read_parquet('s3://bucket/data/')

# Read specific partition (skips others!)
df = dd.read_parquet('s3://bucket/data/')[
    (dd['year'] == 2020) & 
    (dd['month'] == 12)
]

# Read multiple partitions efficiently
df = dd.read_parquet('s3://bucket/data/', 
    filters=[('year', '>', 2019),
             ('country', '==', 'US')]
)
```

**Dask + Parquet:** Automatic predicate pushdown

---

## Slide 9: Compression Options

| Codec           | Speed      | Ratio | Best For     |
|-----------------|------------|-------|--------------|
| uncompressed    | Fastest    | 1x    | Development  |
| snappy          | Fast       | 2-3x  | General purpose |
| gzip            | Medium     | 3-5x  | Balancing act |
| brotli          | Medium     | 4-6x  | Archival     |
| zstd            | Fast-Med   | 3-5x  | Modern standard |

**Recommendation:**
- **snappy**: Good balance, widely supported
- **zstd**: Better compression, fast
- Avoid **gzip** for analytical workloads (slower)

---

## Slide 10: Setting Compression

```python
# Global compression
df.to_parquet(
    'output/',
    compression='zstd',
    compression_level=1  # Balance speed/size
)

# Per-column compression (advanced)
df.to_parquet(
    'output/',
    compression={
        'numeric_cols': 'zstd',
        'text_cols': 'snappy',  # Text compresses differently
        'large_blobs': 'brotli'
    }
)
```

---

## Slide 11: Real-World Example: Weather Data

**Before (CSV):**
- 10GB uncompressed
- Read entire file for any query
- No schema validation
- Slow filters

**Partitioning:**
- `year=YYYY/month=MM/`
- 24 partitions for 2 years
- **50% faster** queries

**After (Parquet):**
- 3GB with snappy (**3.3x reduction**)
- Read only needed columns
- Schema validated on read
- Fast columnar scans

**Compression:**
- snappy: Balanced
- Brotli: **4GB → 1.5GB** (better ratio, slower)

---

## Slide 12: Best Practices: Raw→Bronze→Silver

```python
# Step 1: Raw (untouched)
download_data('raw_data/')

# Step 2: Bronze (schema + compression)
raw = dd.read_csv('raw_data/*.csv')
bronze = (raw
    .assign(date=dd.to_datetime(raw['date']))
    .dropna(subset=['key_cols'])
)
bronze.to_parquet(
    'bronze/',
    partition_on=['year'],
    compression='snappy'
)

# Step 3: Silver (joined + optimized)
bronze = dd.read_parquet('bronze/')
metadata = dd.read_parquet('metadata/')
silver = bronze.merge(metadata, on='station_id')
silver.to_parquet(
    'silver/',
    partition_on=['year', 'country'],
    compression='zstd'
)
```

---

## Slide 13: Choosing Partition Columns

1. **Frequently filtered** (year, month, country)
2. **Balanced cardinality** (not too many, not too few)
3. **Query patterns** match your filters
4. **Avoid high-cardinality** columns (user_id, timestamp)

**Examples:**
- Good: `partition_on=['year', 'state']`
- Bad: `partition_on=['timestamp']` (millions of partitions)
- Good: `partition_on=['year']` then repartition by size

---

## Slide 14: Monitoring Partition Sizes

```python
import pyarrow.parquet as pq

# Check partition sizes
table = pq.read_table('output/')
print(f"Row groups: {table.num_row_groups}")
print(f"Compressed size: {table.nbytes}")
print(f"Rows: {len(table)}")

# Inspect in Dask
df = dd.read_parquet('output/')
df.map_partitions(len).compute()  # Rows per partition
df.npartitions  # Number of partitions
```

**Target:** 128MB - 1GB per partition (for S3)

---

## Slide 15: Summary

### Parquet
Columnar format with schema → Fast analytical queries

### Partitioning
Organize by query patterns → Skip irrelevant data

### Compression
Balance speed vs size (snappy/zstd) → Cost savings

**Dask Integration:**
- Automatic predicate pushdown (filters)
- Column projection (read only needed columns)
- Parallel I/O across partitions
- Lazy evaluation (combine multiple operations)

---

## Slide 16: Questions?

**Demo:** Converting CSV → Parquet with Dask

