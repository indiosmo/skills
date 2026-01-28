---
name: using-pandas
description: "Idiomatic pandas usage patterns and performance best practices. Use when writing or reviewing pandas code to ensure: (1) Modern API usage (loc/iloc, method chaining, pipe), (2) Performance optimization (vectorization, dtypes, avoiding apply), (3) Proper data reshaping (tidy data, melt/pivot), (4) Correct handling of Copy-on-Write, categoricals, time series, (5) Avoiding common gotchas and antipatterns."
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

Never iterate rows when vectorized operations exist:

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

```python
# Bad: Chained indexing (unpredictable behavior)
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

`apply(axis=1)` iterates in Python - extremely slow:

```python
# Bad: Row-wise apply
df['result'] = df.apply(lambda row: row['a'] + row['b'] * 2, axis=1)

# Good: Vectorized
df['result'] = df['a'] + df['b'] * 2
```

### Build DataFrames Efficiently

```python
# Bad: Iterative building (O(n^2))
df = pd.DataFrame()
for item in items:
    df = pd.concat([df, pd.DataFrame([item])])

# Good: Collect then create (O(n))
rows = [item for item in items]
df = pd.DataFrame(rows)
```

### Use pd.concat() Not append

```python
# Combine DataFrames
df = pd.concat([df1, df2, df3], ignore_index=True)
```

### Prefer Built-in GroupBy Methods

```python
# Slow: Custom function
df.groupby('key')['value'].apply(lambda x: x.max() - x.min())

# Fast: Built-in
g = df.groupby('key')['value']
g.max() - g.min()
```

### Choose Appropriate dtypes

```python
# Low-cardinality strings -> category
df['status'] = df['status'].astype('category')

# PyArrow strings (pandas 2.0+)
df['name'] = df['name'].astype('string[pyarrow]')

# Downcast numerics
df['small_int'] = pd.to_numeric(df['small_int'], downcast='integer')
```

See `references/performance.md` for detailed optimization patterns.

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

| File | Contents | When to Consult |
|------|----------|-----------------|
| `references/performance.md` | Optimization patterns | Code running slowly |
| `references/io-formats.md` | File format selection | Reading/writing data |
| `references/timeseries.md` | Time series patterns | Working with dates |
| `references/groupby-window.md` | GroupBy and windows | Split-apply-combine |
