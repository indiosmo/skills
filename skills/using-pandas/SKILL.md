---
name: using-pandas
description: "Activate for ANY task involving tabular data, DataFrames, CSV wrangling, data cleaning, groupby, merge/join, pivot, melt, reshaping, aggregation, or time series analysis -- even if they don't explicitly mention 'pandas' or 'best practices'. Covers idiomatic pandas patterns, performance optimization (vectorization, dtypes, avoiding apply), proper data reshaping (tidy data, melt/pivot), merge/join correctness, Copy-on-Write, categoricals, string operations, and common gotchas."
---

# Pandas Best Practices

Guidelines for writing idiomatic, performant pandas code.

---

## Core Principles

### 1. Tidy Data

Structure data so that:
- Each variable is a column
- Each observation is a row
- Each type of observational unit is a table

```python
# Tidy: one observation per row
# date       | city     | temperature
# 2024-01-01 | NYC      | 32
# 2024-01-01 | LA       | 68

# Not tidy: cities as columns
# date       | NYC  | LA
# 2024-01-01 | 32   | 68

# Convert wide to tidy
df_tidy = df.melt(id_vars=['date'], var_name='city', value_name='temperature')
```

### 2. Method Chaining

Chain operations for readable, debuggable code:

```python
result = (
    df
    .query('age > 25')
    .assign(income_bracket=lambda x: pd.cut(x['income'], bins=5))
    .groupby('income_bracket')
    .agg(count=('id', 'size'), avg_age=('age', 'mean'))
    .reset_index()
)
```

### 3. Vectorization Over Iteration

Never iterate rows when vectorized operations exist. Row iteration drops from vectorized C/NumPy kernels to Python-speed loops, often 100x slower:

```python
# Bad: Row iteration
for idx, row in df.iterrows():
    df.loc[idx, 'result'] = row['a'] + row['b']

# Good: Vectorized
df['result'] = df['a'] + df['b']
```

### 4. Copy-on-Write (pandas 3.0 Default)

Copy-on-Write prevents accidental mutations:

```python
# Pre-CoW (problematic)
df2 = df[df['a'] > 0]
df2['b'] = 1  # May or may not modify df

# With CoW (safe)
df2 = df[df['a'] > 0]
df2['b'] = 1  # Never modifies df

# Enable CoW explicitly (pandas < 3.0)
pd.options.mode.copy_on_write = True
```

---

## Indexing Best Practices

### Always Use .loc and .iloc

| Method | Use For | Slice Behavior |
|--------|---------|----------------|
| `.loc[]` | Labels | Inclusive both ends |
| `.iloc[]` | Positions | Exclusive end |

```python
# Label-based (inclusive)
df.loc['2024-01':'2024-06']  # Includes both Jan and Jun
df.loc[df['col'] > 5, 'target']

# Position-based (exclusive end)
df.iloc[0:5]    # Rows 0-4
df.iloc[:, 0:3] # Columns 0-2
```

### Never Use Chained Indexing

Chained indexing (`df[...][...]`) is ambiguous because intermediate steps may return a view or a copy, so assignments may silently fail:

```python
# Bad: Chained indexing (view vs copy ambiguity)
df[df['a'] > 0]['b'] = 1  # May not work, SettingWithCopyWarning

# Good: Single .loc
df.loc[df['a'] > 0, 'b'] = 1
```

### MultiIndex Slicing

```python
# Use pd.IndexSlice for complex MultiIndex selection
idx = pd.IndexSlice
df.loc[idx['2024', :], :]  # All second-level indices for '2024'
df.loc[idx[:, 'category_a'], 'value']  # Specific second level
```

---

## Performance Patterns

### Avoid DataFrame.apply(axis=1)

`apply(axis=1)` iterates row-by-row in Python rather than dispatching to C/NumPy, typically 100x slower. Replace with vectorized operations:

```python
# Bad: Row-wise apply
df['result'] = df.apply(lambda row: row['a'] + row['b'] * 2, axis=1)

# Good: Vectorized
df['result'] = df['a'] + df['b'] * 2
```

`apply` is acceptable for: column-wise operations (`axis=0`, which is already vectorized), complex string operations not available in the `.str` accessor, and multi-column logic that genuinely resists vectorization (but try `np.where`/`np.select` first).

### Key Performance Rules

- **Build DataFrames in one shot**: collect rows in a list, then `pd.DataFrame(rows)`. Iterative `concat` is O(n^2).
- **Use built-in GroupBy methods** (`sum`, `mean`, `max`) over `.apply()` with lambdas.
- **Choose appropriate dtypes**: `category` for low-cardinality strings, `string[pyarrow]` for general strings (pandas 2.0+), `pd.to_numeric(..., downcast='integer')` for numerics.

See `references/performance.md` for the full catalog of optimization patterns.

---

## Data Reshaping

### Melt: Wide to Long

```
BEFORE (wide):                      AFTER (long):
id | name  | 2022 | 2023            id | name  | year | value
---+-------+------+------           ---+-------+------+-------
1  | Alice | 100  | 120             1  | Alice | 2022 | 100
2  | Bob   | 200  | 250             1  | Alice | 2023 | 120
                                    2  | Bob   | 2022 | 200
                                    2  | Bob   | 2023 | 250
```

```python
df_long = pd.melt(
    df,
    id_vars=['id', 'name'],      # Keep as columns
    value_vars=['2022', '2023'], # Convert to rows
    var_name='year',
    value_name='value'
)
```

### Pivot: Long to Wide

```
BEFORE (long):                      AFTER (wide):
id | year | value                   id | 2022 | 2023
---+------+-------                  ---+------+------
1  | 2022 | 100                     1  | 100  | 120
1  | 2023 | 120                     2  | 200  | 250
2  | 2022 | 200
2  | 2023 | 250
```

```python
df_wide = df.pivot(
    index='id',
    columns='year',
    values='value'
)

# With aggregation (handles duplicates)
df_wide = df.pivot_table(
    index='id',
    columns='year',
    values='value',
    aggfunc='sum'
)
```

### Adding Columns in Chains

```python
# Use assign() for method chaining
df = (
    df
    .assign(
        total=lambda x: x['a'] + x['b'],
        ratio=lambda x: x['a'] / x['total']
    )
)
```

---

## Merging and Joining

### Join Types

```python
# Inner: only matching keys (default)
pd.merge(left, right, on='key', how='inner')

# Left: all left rows, matched right rows (NaN where no match)
pd.merge(left, right, on='key', how='left')

# Right: all right rows, matched left rows
pd.merge(left, right, on='key', how='right')

# Outer: all rows from both sides
pd.merge(left, right, on='key', how='outer')
```

### Catching Many-to-Many with validate

Use `validate` to assert the expected join cardinality. Without it, accidental many-to-many joins silently explode row counts:

```python
pd.merge(orders, customers, on='customer_id', validate='many_to_one')
# Options: 'one_to_one', 'one_to_many', 'many_to_one', 'many_to_many'
```

### Key Dtype Mismatches

Merges produce zero matches when key columns have different dtypes (e.g., `int64` vs `object`). Always align dtypes before merging:

```python
# If left has int keys and right has string keys
right['key'] = right['key'].astype(int)
pd.merge(left, right, on='key')
```

### Overlapping Column Names

When both DataFrames share non-key column names, use `suffixes` to disambiguate:

```python
pd.merge(left, right, on='key', suffixes=('_left', '_right'))
```

---

## String Operations

Use the `.str` accessor for vectorized string operations instead of `apply` with Python string methods:

```python
# Pattern matching
df[df['name'].str.contains('smith', case=False, na=False)]

# Extract with regex capture groups
df['area_code'] = df['phone'].str.extract(r'\((\d{3})\)')

# Replace patterns
df['clean'] = df['text'].str.replace(r'\s+', ' ', regex=True)

# Other common operations
df['name'].str.lower()
df['name'].str.strip()
df['name'].str.split(',', expand=True)
df['name'].str.len()
```

---

## Common Gotchas

### Truth Value Ambiguity

```python
# Error: Ambiguous truth value
if df['col'] > 5:  # Series has multiple values
    pass

# Solution: Use .any() or .all()
if (df['col'] > 5).any():
    pass

# For boolean operations, use bitwise operators
df[(df['a'] > 5) & (df['b'] < 10)]  # Not 'and'
df[(df['a'] > 5) | (df['b'] < 10)]  # Not 'or'
```

### The `in` Operator Tests Index

```python
# This checks the INDEX, not values
'value' in df['col']  # Wrong!

# Check values with .isin() or .values
'value' in df['col'].values  # Correct
df['col'].isin(['value'])    # For multiple values
```

### Integer Coercion with NaN

```python
# Integers become float when NaN is present
df['int_col'] = [1, 2, None, 4]  # dtype: float64

# Use nullable integer type
df['int_col'] = pd.array([1, 2, None, 4], dtype='Int64')  # Capital I
```

### Chained Assignment

Same view-vs-copy ambiguity as chained indexing. The first expression may return a copy, so the assignment is lost:

```python
# May fail silently
df[df['a'] > 0]['b'] = 1

# Always use single .loc
df.loc[df['a'] > 0, 'b'] = 1
```

### Comparing with None

```python
# Wrong: Comparison with None
df[df['col'] == None]  # Doesn't work as expected

# Correct: Use isna/notna
df[df['col'].isna()]
df[df['col'].notna()]
```

---

## Method Chaining with pipe()

For custom functions in chains:

```python
def add_features(df, multiplier=2):
    return df.assign(
        doubled=df['value'] * multiplier,
        log_value=np.log1p(df['value'])
    )

result = (
    df
    .query('active == True')
    .pipe(add_features, multiplier=3)
    .groupby('category')
    .agg({'doubled': 'mean'})
)
```

---

## Quick Reference

### Selection Patterns

| Task | Code |
|------|------|
| Filter rows | `df.query('col > 5')` or `df[df['col'] > 5]` |
| Select columns | `df[['a', 'b']]` or `df.loc[:, ['a', 'b']]` |
| Filter + select | `df.loc[df['a'] > 5, ['b', 'c']]` |
| By dtype | `df.select_dtypes(include=['number'])` |

### Aggregation Patterns

| Task | Code |
|------|------|
| Group aggregate | `df.groupby('key').agg(total=('val', 'sum'))` |
| Group transform | `df.groupby('key')['val'].transform('mean')` |
| Rolling | `df['val'].rolling(7).mean()` |
| Expanding | `df['val'].expanding().sum()` |

### Reshaping Patterns

| Task | Code |
|------|------|
| Wide to long | `pd.melt(df, id_vars=['id'], value_vars=['a', 'b'])` |
| Long to wide | `df.pivot(index='id', columns='key', values='val')` |
| Add column | `df.assign(new=lambda x: x['a'] + x['b'])` |
| Concatenate | `pd.concat([df1, df2], ignore_index=True)` |

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/performance.md` | Read when code is slow, when choosing dtypes, when building DataFrames from loops, or when deciding between `apply` vs vectorization. |
| `references/io-formats.md` | Read when choosing between CSV/Parquet/Feather/JSON/Excel, when reading large files in chunks, or when configuring cloud/remote file access. |
| `references/timeseries.md` | Read when working with DatetimeIndex, resampling frequencies, rolling/expanding windows on dates, timezone handling, or period arithmetic. |
| `references/groupby-window.md` | Read when writing groupby aggregations, transforms, or filters; when combining groupby with rolling/expanding windows; or when building ranked/cumulative columns per group. |
