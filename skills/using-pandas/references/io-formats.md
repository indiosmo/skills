# I/O Best Practices and Format Selection

Guidelines for reading and writing data efficiently.

---

## Format Selection Guide

| Format | Best For | Read Speed | Write Speed | File Size |
|--------|----------|------------|-------------|-----------|
| **Parquet** | Analytics, large data | Fast | Fast | Small (compressed) |
| **Feather** | Fast interchange | Fastest | Fastest | Medium |
| **CSV** | Interop, small data | Slow | Medium | Large |
| **JSON** | APIs, nested data | Slow | Slow | Large |
| **Pickle** | Python-only caching | Fast | Fast | Medium |
| **HDF5** | Scientific data | Fast | Fast | Medium |

### When to Use Each

**Parquet** (Default choice for analytics)
- Columnar format - reads only needed columns
- Excellent compression
- Preserves dtypes including categoricals
- Works with Dask, Spark, DuckDB

**Feather** (Fast local interchange)
- Fastest read/write for pandas
- No compression overhead
- Good for temporary files and caching
- Arrow-native format

**CSV** (Interoperability)
- Universal compatibility
- Human readable
- Use only when required for external tools
- Always specify dtypes when reading

---

## Reading CSV Efficiently

### Specify dtypes Upfront

```python
# Avoid dtype inference (slow and memory-intensive)
dtypes = {
    'id': 'int32',
    'name': 'string',
    'category': 'category',
    'value': 'float32',
    'date': 'string'  # Parse dates separately
}

df = pd.read_csv('data.csv', dtype=dtypes)
df['date'] = pd.to_datetime(df['date'])
```

### Read Only Needed Columns

```python
# Don't read columns you won't use
df = pd.read_csv('data.csv', usecols=['id', 'name', 'value'])
```

### Use Appropriate Engine

```python
# 'c' engine: Default, fast, most features
df = pd.read_csv('data.csv', engine='c')

# 'pyarrow' engine: Faster for large files (pandas 1.4+)
df = pd.read_csv('data.csv', engine='pyarrow')

# 'python' engine: Slower, but handles edge cases
df = pd.read_csv('malformed.csv', engine='python', on_bad_lines='skip')
```

### Handle Large Files

```python
# Process in chunks
chunks = pd.read_csv('huge.csv', chunksize=100_000)
processed = pd.concat([
    process_chunk(chunk)
    for chunk in chunks
])

# Or aggregate without loading full data
total = 0
for chunk in pd.read_csv('huge.csv', chunksize=100_000):
    total += chunk['value'].sum()
```

### Common Parameters

```python
df = pd.read_csv(
    'data.csv',
    dtype=dtypes,              # Explicit types
    usecols=['col1', 'col2'],  # Limit columns
    nrows=1000,                # Limit rows (for testing)
    skiprows=1,                # Skip header rows
    na_values=['NA', 'N/A'],   # Custom NA values
    parse_dates=['date_col'],  # Parse dates (slow, consider post-processing)
    index_col='id',            # Set index directly
    low_memory=False           # Avoid mixed type warnings
)
```

---

## Reading Parquet

### Basic Usage

```python
# Simple read
df = pd.read_parquet('data.parquet')

# Read specific columns (only reads those from disk)
df = pd.read_parquet('data.parquet', columns=['id', 'value'])

# Read with filters (predicate pushdown)
df = pd.read_parquet(
    'data.parquet',
    filters=[('year', '==', 2024), ('status', 'in', ['active', 'pending'])]
)
```

### Directory of Parquet Files

```python
# Read partitioned dataset
df = pd.read_parquet('data/')  # Reads all .parquet files

# With specific engine
df = pd.read_parquet('data/', engine='pyarrow')
```

### Use PyArrow Backend

```python
# Returns PyArrow-backed DataFrame (pandas 2.0+)
df = pd.read_parquet('data.parquet', dtype_backend='pyarrow')
```

---

## Writing Parquet

```python
# Basic write
df.to_parquet('output.parquet')

# With compression (default is snappy)
df.to_parquet('output.parquet', compression='zstd')  # Better compression
df.to_parquet('output.parquet', compression='gzip')  # Wider compatibility

# Partitioned output
df.to_parquet('output/', partition_cols=['year', 'month'])
```

---

## Reading/Writing Feather

```python
# Write
df.to_feather('data.feather')

# Read
df = pd.read_feather('data.feather')

# Read specific columns
df = pd.read_feather('data.feather', columns=['id', 'value'])
```

Use Feather for:
- Caching intermediate results
- Fast data exchange between Python processes
- When you need fastest possible I/O

---

## Remote File Access

### Read from URLs

```python
# HTTP/HTTPS
df = pd.read_csv('https://example.com/data.csv')

# S3 (requires s3fs)
df = pd.read_parquet('s3://bucket/data.parquet')

# GCS (requires gcsfs)
df = pd.read_parquet('gs://bucket/data.parquet')

# Azure (requires adlfs)
df = pd.read_parquet('abfs://container/data.parquet')
```

### Configure Cloud Access

```python
# S3 with credentials
import s3fs
fs = s3fs.S3FileSystem(
    key='access_key',
    secret='secret_key'
)
df = pd.read_parquet('s3://bucket/data.parquet', filesystem=fs)

# Or use environment variables
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
df = pd.read_parquet('s3://bucket/data.parquet')
```

---

## Excel Files

### Reading Excel

```python
# Basic read
df = pd.read_excel('data.xlsx')

# Specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet2')

# Multiple sheets
dfs = pd.read_excel('data.xlsx', sheet_name=['Sheet1', 'Sheet2'])
# Returns dict: {'Sheet1': df1, 'Sheet2': df2}

# All sheets
dfs = pd.read_excel('data.xlsx', sheet_name=None)
```

### Writing Excel

```python
# Single sheet
df.to_excel('output.xlsx', index=False)

# Multiple sheets
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Data')
    df2.to_excel(writer, sheet_name='Summary')
```

**Note:** Excel I/O is slow. Convert to Parquet for analysis, export to Excel only for final delivery.

---

## JSON

### Reading JSON

```python
# Standard JSON array
df = pd.read_json('data.json')

# Line-delimited JSON (one object per line)
df = pd.read_json('data.jsonl', lines=True)

# Nested JSON - normalize
import json
with open('nested.json') as f:
    data = json.load(f)
df = pd.json_normalize(data, record_path='items', meta=['id', 'name'])
```

### Writing JSON

```python
# Standard format
df.to_json('output.json', orient='records')

# Line-delimited (better for large files)
df.to_json('output.jsonl', orient='records', lines=True)
```

---

## Best Practices Summary

1. **Default to Parquet** for any non-trivial data analysis
2. **Use Feather** for caching and fast temporary storage
3. **Specify dtypes** when reading CSV - never rely on inference for production
4. **Read only needed columns** - especially important for Parquet
5. **Use PyArrow engine/backend** when available (pandas 2.0+)
6. **Chunk large files** that don't fit in memory
7. **Convert CSV to Parquet** early in your pipeline
8. **Partition large datasets** by commonly-filtered columns
