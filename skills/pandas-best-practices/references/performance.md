# Performance Optimization Patterns

Guidelines for writing fast pandas code.

---

## Constructor Patterns

### Use pd.concat(), Not Iterative Append

**Bad - O(n^2) complexity:**
```python
df = pd.DataFrame()
for item in items:
    df = pd.concat([df, pd.DataFrame([item])])  # Creates new DataFrame each time
```

**Good - O(n) complexity:**
```python
# Collect in list, concat once
rows = []
for item in items:
    rows.append(item)
df = pd.DataFrame(rows)

# Or use list comprehension
df = pd.DataFrame([process(item) for item in items])
```

### Preallocate When Size Known

```python
# When you know the final size
df = pd.DataFrame(index=range(n), columns=['a', 'b', 'c'])
for i, item in enumerate(items):
    df.iloc[i] = [item.a, item.b, item.c]
```

---

## Vectorization Over Iteration

### Avoid DataFrame.apply(axis=1)

`apply(axis=1)` iterates row by row in Python - extremely slow.

**Bad:**
```python
df['result'] = df.apply(lambda row: row['a'] + row['b'] * row['c'], axis=1)
```

**Good - Vectorized:**
```python
df['result'] = df['a'] + df['b'] * df['c']
```

### Use NumPy for Complex Operations

```python
# Conditional assignment
df['category'] = np.where(df['value'] > 100, 'high', 'low')

# Multiple conditions
df['tier'] = np.select(
    [df['value'] > 1000, df['value'] > 100, df['value'] > 10],
    ['platinum', 'gold', 'silver'],
    default='bronze'
)

# Clip values
df['clipped'] = np.clip(df['value'], 0, 100)
```

### When apply() Is Acceptable

- Column-wise operations: `df.apply(func, axis=0)` is vectorized
- Complex string operations not in `.str` accessor
- Operations requiring multiple columns with complex logic (but try vectorization first)

---

## Dtype Optimization

### Use Appropriate Numeric Types

```python
# Check memory usage
df.info(memory_usage='deep')

# Downcast integers
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')

# Downcast floats
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')
```

| Type | Range | Memory |
|------|-------|--------|
| int8 | -128 to 127 | 1 byte |
| int16 | -32,768 to 32,767 | 2 bytes |
| int32 | -2.1B to 2.1B | 4 bytes |
| int64 | Full range | 8 bytes |

### Use Categoricals for Low-Cardinality Strings

**When to use:** Column has repeated string values (< 50% unique)

```python
# Convert existing column
df['status'] = df['status'].astype('category')

# Read with category dtype
df = pd.read_csv('file.csv', dtype={'status': 'category'})

# Memory comparison
df['status_str'] = df['status'].astype('object')
df['status_cat'] = df['status'].astype('category')
print(df['status_str'].memory_usage(deep=True))  # Large
print(df['status_cat'].memory_usage(deep=True))  # Much smaller
```

### Use PyArrow Backend (pandas 2.0+)

```python
# Enable PyArrow strings (much faster)
df = pd.read_csv('file.csv', dtype_backend='pyarrow')

# Or convert existing
df['col'] = df['col'].astype('string[pyarrow]')
```

Benefits:
- Faster string operations
- Better memory efficiency
- Native null support

---

## GroupBy Optimization

### Prefer Built-in Methods Over UDFs

**Slow - Custom function:**
```python
df.groupby('key')['value'].apply(lambda x: x.max() - x.min())
```

**Fast - Built-in methods:**
```python
grouped = df.groupby('key')['value']
grouped.max() - grouped.min()
```

### Use transform() Correctly

```python
# Adds group statistics back to original DataFrame
df['group_mean'] = df.groupby('key')['value'].transform('mean')
df['normalized'] = df['value'] / df.groupby('key')['value'].transform('sum')
```

### Named Aggregation (pandas 0.25+)

```python
# Clean, efficient syntax
df.groupby('key').agg(
    total=('value', 'sum'),
    average=('value', 'mean'),
    count=('id', 'nunique')
)
```

---

## Algorithm Selection

### Use nlargest/nsmallest Instead of Sort

**Slow - Full sort O(n log n):**
```python
df.sort_values('value', ascending=False).head(10)
```

**Fast - Partial sort O(n):**
```python
df.nlargest(10, 'value')
```

### Use isin() for Multiple Equality Checks

**Slow:**
```python
df[(df['col'] == 'a') | (df['col'] == 'b') | (df['col'] == 'c')]
```

**Fast:**
```python
df[df['col'].isin(['a', 'b', 'c'])]
```

### Use query() for Complex Filters

```python
# More readable and can be faster for large DataFrames
df.query('age > 25 and status == "active"')

# With variables
min_age = 25
df.query('age > @min_age')
```

---

## Memory Management

### Read Only Needed Columns

```python
# Specify columns upfront
df = pd.read_csv('large.csv', usecols=['col1', 'col2', 'col3'])
```

### Process in Chunks

```python
# For files larger than memory
chunks = pd.read_csv('huge.csv', chunksize=100_000)
results = []
for chunk in chunks:
    processed = process(chunk)
    results.append(processed)
final = pd.concat(results)
```

### Release Memory

```python
# Delete and collect
del df
import gc
gc.collect()

# Or reassign to smaller
df = df[df['active']]  # Filter reduces size
```

---

## Index Optimization

### Set Index for Repeated Lookups

```python
# If you frequently filter by a column
df = df.set_index('id')
df.loc[12345]  # O(1) lookup

# For time series
df = df.set_index('timestamp')
df.loc['2024-01-01':'2024-01-31']  # Fast date range selection
```

### Sort Index for Range Queries

```python
# Sorting enables faster slicing
df = df.sort_index()
```

---

## Scaling Beyond pandas

### When pandas Isn't Enough

| Symptom | Solution |
|---------|----------|
| Data doesn't fit in memory | Dask, Polars, or chunked processing |
| Single operations are slow | Polars (Rust-based, faster) |
| Need distributed computing | Dask, Spark |
| GPU acceleration needed | cuDF (RAPIDS) |

### Dask Example

```python
import dask.dataframe as dd

# Lazy loading - doesn't read until compute()
ddf = dd.read_parquet('huge_data/*.parquet')

# Same pandas API
result = ddf.groupby('key')['value'].mean().compute()
```

---

## Profiling

### Measure Before Optimizing

```python
# Time operations
%timeit df.apply(func, axis=1)
%timeit vectorized_version(df)

# Profile memory
%memit df = pd.read_csv('file.csv')

# Line profiler for functions
%lprun -f my_function my_function(df)
```

### Common Bottlenecks

1. `apply(axis=1)` - Replace with vectorization
2. String columns as object dtype - Use category or PyArrow
3. Iterative DataFrame building - Collect in list, concat once
4. Unnecessary copies - Use Copy-on-Write, avoid `.copy()` unless needed
5. Full sorts for top-N - Use nlargest/nsmallest
