# GroupBy and Window Operations

Patterns for split-apply-combine and windowed computations.

---

## GroupBy Fundamentals

GroupBy implements split-apply-combine:
1. **Split**: Divide data into groups
2. **Apply**: Apply function to each group
3. **Combine**: Combine results

```python
# Basic pattern
grouped = df.groupby('category')
result = grouped['value'].mean()
```

---

## Aggregation

Aggregation reduces each group to a single value.

### Single Aggregation

```python
df.groupby('key')['value'].sum()
df.groupby('key')['value'].mean()
df.groupby('key')['value'].count()
df.groupby('key')['value'].nunique()
df.groupby('key')['value'].first()
df.groupby('key')['value'].last()
```

### Multiple Aggregations

```python
# Multiple functions on one column
df.groupby('key')['value'].agg(['sum', 'mean', 'std'])

# Different functions per column
df.groupby('key').agg({
    'value': 'sum',
    'count': 'mean',
    'date': 'max'
})
```

### Named Aggregation (Preferred)

```python
df.groupby('key').agg(
    total=('value', 'sum'),
    average=('value', 'mean'),
    unique_items=('item', 'nunique'),
    latest=('date', 'max')
)
```

Benefits:
- Clear column names in output
- No MultiIndex columns
- Easy to read and maintain

---

## Transformation

Transformation returns data with the same shape as input.

```python
# Group mean broadcast back to original rows
df['group_mean'] = df.groupby('key')['value'].transform('mean')

# Normalize within groups
df['normalized'] = df.groupby('key')['value'].transform(
    lambda x: (x - x.mean()) / x.std()
)

# Rank within groups
df['rank'] = df.groupby('key')['value'].transform('rank')

# Cumulative sum within groups
df['cumsum'] = df.groupby('key')['value'].transform('cumsum')
```

### Common Transform Operations

| Operation | Result |
|-----------|--------|
| `transform('mean')` | Group mean for each row |
| `transform('sum')` | Group sum for each row |
| `transform('rank')` | Rank within group |
| `transform('cumsum')` | Running sum within group |
| `transform('pct_change')` | Percent change within group |

---

## Filtration

Filter keeps or removes entire groups.

```python
# Keep groups where mean > 10
df.groupby('key').filter(lambda x: x['value'].mean() > 10)

# Keep groups with at least 5 members
df.groupby('key').filter(lambda x: len(x) >= 5)

# Keep groups where max < 100
df.groupby('key').filter(lambda x: x['value'].max() < 100)
```

---

## Grouping by Multiple Columns

```python
# Group by multiple keys
df.groupby(['region', 'product'])['sales'].sum()

# Results in MultiIndex - reset if needed
df.groupby(['region', 'product'])['sales'].sum().reset_index()

# Named agg with multiple keys
df.groupby(['region', 'product']).agg(
    total_sales=('sales', 'sum'),
    avg_price=('price', 'mean')
).reset_index()
```

---

## Grouping Options

### Keep NA Groups

```python
# By default, NA keys are excluded
df.groupby('key', dropna=False)['value'].mean()
```

### Preserve Original Order

```python
# Results in first-seen order (not sorted)
df.groupby('key', sort=False)['value'].mean()
```

### Group by Index Level

```python
# With MultiIndex
df.groupby(level=0)['value'].mean()
df.groupby(level='region')['value'].mean()
```

### Group by Function

```python
# Group by result of function applied to index
df.groupby(df.index.month)['value'].mean()

# Or with lambda
df.groupby(lambda x: x.year)['value'].sum()
```

---

## GroupBy + Apply

For complex operations that don't fit agg/transform/filter:

```python
# Custom function per group
def process_group(group):
    return group.nlargest(3, 'value')

df.groupby('key').apply(process_group)

# Return scalar per group (like agg)
df.groupby('key')['value'].apply(lambda x: x.max() - x.min())
```

**Warning:** `apply` is slower than built-in methods. Use agg/transform when possible.

---

## Window Operations

### Rolling Windows

```python
# Basic rolling
df['rolling_mean'] = df['value'].rolling(7).mean()
df['rolling_sum'] = df['value'].rolling(7).sum()
df['rolling_std'] = df['value'].rolling(7).std()

# Min periods for partial windows
df['rolling_mean'] = df['value'].rolling(7, min_periods=1).mean()
```

### Expanding Windows

```python
# Cumulative (all previous rows)
df['cumsum'] = df['value'].expanding().sum()
df['cummax'] = df['value'].expanding().max()
df['cummean'] = df['value'].expanding().mean()
```

### Exponential Weighted

```python
# Recent values weighted more heavily
df['ewm'] = df['value'].ewm(span=7).mean()
```

---

## GroupBy + Window (Rolling by Group)

Combine groupby with window functions:

```python
# Rolling mean within each group
df['group_rolling_mean'] = df.groupby('key')['value'].transform(
    lambda x: x.rolling(7, min_periods=1).mean()
)

# Expanding sum by group
df['group_cumsum'] = df.groupby('key')['value'].cumsum()

# Rank within group (no need for transform)
df['group_rank'] = df.groupby('key')['value'].rank()

# Shift within group
df['prev_value'] = df.groupby('key')['value'].shift(1)
```

### Rolling Window Aggregation

```python
# 7-day rolling count per group
df['rolling_count'] = df.groupby('key')['value'].transform(
    lambda x: x.rolling('7D').count()
)
```

---

## Common Patterns

### Percentage of Group Total

```python
df['pct_of_group'] = df['value'] / df.groupby('key')['value'].transform('sum')
```

### Deviation from Group Mean

```python
df['deviation'] = df['value'] - df.groupby('key')['value'].transform('mean')
```

### Flag Top N per Group

```python
df['is_top_3'] = df.groupby('key')['value'].rank(ascending=False) <= 3
```

### First/Last Row per Group

```python
# First row
df.groupby('key').first()

# Last row
df.groupby('key').last()

# Nth row
df.groupby('key').nth(2)  # Third row (0-indexed)

# With specific column
df.loc[df.groupby('key')['date'].idxmax()]  # Row with max date per group
```

### Mode per Group

```python
df.groupby('key')['category'].agg(lambda x: x.mode().iloc[0])
```

### Running Difference within Group

```python
df['change'] = df.groupby('key')['value'].diff()
```

---

## Performance Tips

1. **Use built-in aggregations** instead of `apply` with lambdas
2. **Named aggregation** is cleaner and equally fast
3. **Transform with built-in functions** is optimized
4. For large data, **sort=False** can improve performance
5. **Categorical keys** speed up groupby significantly

```python
# Convert string keys to categorical before grouping
df['key'] = df['key'].astype('category')
df.groupby('key')['value'].sum()
```
