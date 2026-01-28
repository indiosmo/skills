# Pandas Quick Reference Cheatsheet

Quick reference for common pandas operations.

---

## Creating DataFrames

```python
# From dictionary
df = pd.DataFrame({
    'col1': [1, 2, 3],
    'col2': ['a', 'b', 'c']
})

# From list of dicts
df = pd.DataFrame([
    {'col1': 1, 'col2': 'a'},
    {'col1': 2, 'col2': 'b'}
])

# With explicit index
df = pd.DataFrame(data, index=['row1', 'row2', 'row3'])

# From CSV
df = pd.read_csv('file.csv', dtype={'col': 'category'})

# From Parquet (preferred for large data)
df = pd.read_parquet('file.parquet')
```

---

## Subsetting Rows

```python
# By condition (boolean indexing)
df[df['col'] > 5]
df[df['col'].isin(['a', 'b'])]
df[df['col'].str.contains('pattern')]

# By position
df.iloc[0:5]           # First 5 rows
df.iloc[[0, 2, 4]]     # Specific positions

# By label
df.loc['row_label']
df.loc['start':'end']  # Inclusive on both ends

# Largest/smallest
df.nlargest(5, 'col')  # Top 5 by column
df.nsmallest(5, 'col')
```

---

## Subsetting Columns

```python
# Single column (returns Series)
df['col']
df.col              # Avoid: breaks with spaces/keywords

# Multiple columns (returns DataFrame)
df[['col1', 'col2']]

# By dtype
df.select_dtypes(include=['number'])
df.select_dtypes(exclude=['object'])

# Pattern matching
df.filter(like='prefix_')
df.filter(regex=r'^col\d+$')
```

---

## Subsetting Rows and Columns

```python
# .loc - label-based (inclusive)
df.loc[df['a'] > 5, ['b', 'c']]
df.loc['row1':'row3', 'col1':'col3']

# .iloc - position-based (exclusive end)
df.iloc[0:5, 0:3]
df.iloc[[0, 2], [1, 3]]

# Combined
df.loc[df['a'] > 5, 'b']  # Returns Series
```

---

## Reshaping Data

### Melt (Wide to Long)

```python
# Convert columns to rows
pd.melt(df,
    id_vars=['id'],           # Keep these as columns
    value_vars=['2020', '2021'],  # Stack these
    var_name='year',          # Name for variable column
    value_name='value'        # Name for value column
)
```

### Pivot (Long to Wide)

```python
# Convert rows to columns
df.pivot(
    index='id',       # Row identifier
    columns='year',   # Column to spread
    values='value'    # Values to fill
)

# With aggregation
df.pivot_table(
    index='id',
    columns='year',
    values='value',
    aggfunc='mean'    # Handle duplicates
)
```

### Stack/Unstack

```python
# Stack: columns to MultiIndex rows
df.stack()

# Unstack: MultiIndex rows to columns
df.unstack()
df.unstack(level=0)  # Specific level
```

---

## Combining DataFrames

### Concatenation

```python
# Vertical (stack rows)
pd.concat([df1, df2], ignore_index=True)

# Horizontal (add columns)
pd.concat([df1, df2], axis=1)
```

### Joins

```python
# Merge (SQL-style)
pd.merge(df1, df2, on='key')
pd.merge(df1, df2, left_on='a', right_on='b')
pd.merge(df1, df2, on='key', how='left')  # left/right/outer/inner

# Join on index
df1.join(df2, how='left')
```

### Set Operations

```python
pd.concat([df1, df2]).drop_duplicates()  # Union
df1[df1['key'].isin(df2['key'])]         # Intersection
df1[~df1['key'].isin(df2['key'])]        # Difference
```

---

## Summary Statistics

```python
# Single statistics
df['col'].sum()
df['col'].mean()
df['col'].median()
df['col'].std()
df['col'].min() / df['col'].max()
df['col'].quantile([0.25, 0.5, 0.75])

# Multiple statistics
df.describe()                    # Numeric columns
df.describe(include='all')       # All columns
df['col'].value_counts()         # Frequency
df['col'].nunique()              # Unique count

# By group
df.groupby('cat')['val'].mean()
df.groupby('cat').agg({'val': ['mean', 'std']})
```

---

## Adding/Modifying Columns

```python
# Direct assignment
df['new'] = df['a'] + df['b']

# In method chain
df.assign(
    new_col=lambda x: x['a'] + x['b'],
    other=lambda x: x['new_col'] * 2
)

# Conditional
df['category'] = np.where(df['val'] > 10, 'high', 'low')

# Multiple conditions
df['tier'] = np.select(
    [df['val'] > 100, df['val'] > 50],
    ['gold', 'silver'],
    default='bronze'
)
```

---

## String Operations

```python
# Access via .str accessor
df['col'].str.lower()
df['col'].str.upper()
df['col'].str.strip()
df['col'].str.replace('old', 'new')
df['col'].str.split('_', expand=True)
df['col'].str.contains('pattern', regex=True)
df['col'].str.extract(r'(\d+)')
df['col'].str.len()
```

---

## Datetime Operations

```python
# Parse dates
df['date'] = pd.to_datetime(df['date_str'])

# Access via .dt accessor
df['date'].dt.year
df['date'].dt.month
df['date'].dt.day
df['date'].dt.dayofweek
df['date'].dt.quarter
df['date'].dt.date        # Date only (no time)

# Date arithmetic
df['date'] + pd.Timedelta(days=7)
df['date'] - df['other_date']  # Returns Timedelta

# Resampling (with DatetimeIndex)
df.resample('M').mean()   # Monthly
df.resample('Q').sum()    # Quarterly
```

---

## Missing Data

```python
# Detection
df.isna()           # Boolean mask
df.isna().sum()     # Count per column
df.notna()

# Removal
df.dropna()                    # Any missing
df.dropna(subset=['col'])      # Specific columns
df.dropna(thresh=3)            # Keep rows with 3+ non-null

# Filling
df.fillna(0)
df.fillna(method='ffill')      # Forward fill
df.fillna(df.mean())           # Fill with mean
df['col'].interpolate()        # Interpolate
```

---

## Sorting

```python
# By values
df.sort_values('col')
df.sort_values('col', ascending=False)
df.sort_values(['col1', 'col2'], ascending=[True, False])

# By index
df.sort_index()
df.sort_index(ascending=False)
```

---

## Groupby Quick Reference

```python
# Basic
df.groupby('key')['val'].mean()

# Multiple columns
df.groupby(['key1', 'key2'])['val'].sum()

# Multiple aggregations
df.groupby('key').agg(
    total=('val', 'sum'),
    avg=('val', 'mean'),
    count=('val', 'size')
)

# Transform (returns same shape)
df['normalized'] = df.groupby('key')['val'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Filter groups
df.groupby('key').filter(lambda x: x['val'].mean() > 10)
```
