# Time Series Handling Patterns

Best practices for working with time series data in pandas.

---

## DatetimeIndex Fundamentals

### Creating DatetimeIndex

```python
# From strings
df['date'] = pd.to_datetime(df['date_str'])

# Set as index
df = df.set_index('date')

# Or create with index directly
df = pd.DataFrame(data, index=pd.to_datetime(dates))

# Generate date range
idx = pd.date_range('2024-01-01', periods=100, freq='D')
idx = pd.date_range('2024-01-01', '2024-12-31', freq='ME')  # Month ends
```

### Common Frequencies

| Code | Meaning |
|------|---------|
| `D` | Calendar day |
| `B` | Business day |
| `W` | Weekly (Sunday) |
| `W-MON` | Weekly (Monday) |
| `ME` | Month end |
| `MS` | Month start |
| `QE` | Quarter end |
| `YE` | Year end |
| `h` | Hourly |
| `min` | Minutely |
| `s` | Secondly |

---

## Partial String Indexing

With a DatetimeIndex, select data using partial strings:

```python
# Assuming df has DatetimeIndex
df.loc['2024']              # All of 2024
df.loc['2024-03']           # March 2024
df.loc['2024-03-15']        # Single day
df.loc['2024-01':'2024-06'] # First half of 2024

# Time component
df.loc['2024-03-15 09']     # 9 AM hour on March 15
df.loc['2024-03-15 09:30']  # Specific minute
```

**Note:** Partial string indexing only works with DatetimeIndex, not datetime columns.

---

## Resampling

Resample changes the frequency of time series data.

### Downsampling (Higher to Lower Frequency)

```python
# Daily to monthly (aggregate)
df.resample('ME').mean()      # Monthly average
df.resample('ME').sum()       # Monthly total
df.resample('ME').last()      # Last value each month

# Multiple aggregations
df.resample('ME').agg({
    'price': 'mean',
    'volume': 'sum',
    'high': 'max',
    'low': 'min'
})
```

### Upsampling (Lower to Higher Frequency)

```python
# Monthly to daily (need to fill gaps)
df.resample('D').ffill()      # Forward fill
df.resample('D').bfill()      # Backward fill
df.resample('D').interpolate() # Linear interpolation

# Fill only recent gaps
df.resample('D').ffill(limit=5)
```

### OHLC Resampling

```python
# Standard OHLC from transaction data
ohlc = df['price'].resample('D').ohlc()
# Returns: open, high, low, close columns
```

---

## Rolling Windows

### Basic Rolling

```python
# 7-day rolling mean
df['rolling_mean'] = df['value'].rolling(7).mean()

# With minimum periods (for start of series)
df['rolling_mean'] = df['value'].rolling(7, min_periods=1).mean()

# Centered window
df['rolling_mean'] = df['value'].rolling(7, center=True).mean()
```

### Time-Based Windows

```python
# 7 days (not 7 rows)
df['rolling_7d'] = df['value'].rolling('7D').mean()

# Requires DatetimeIndex and sorted data
df = df.sort_index()
```

### Common Rolling Operations

```python
df['roll_sum'] = df['value'].rolling(7).sum()
df['roll_std'] = df['value'].rolling(7).std()
df['roll_min'] = df['value'].rolling(7).min()
df['roll_max'] = df['value'].rolling(7).max()

# Rolling correlation
df['corr'] = df['a'].rolling(30).corr(df['b'])
```

---

## Expanding Windows

Expanding includes all previous observations.

```python
# Cumulative statistics
df['cumsum'] = df['value'].expanding().sum()
df['cummean'] = df['value'].expanding().mean()
df['cummax'] = df['value'].expanding().max()

# Running count of observations
df['count'] = df['value'].expanding().count()
```

---

## Exponential Weighted Moving Average (EWMA)

Gives more weight to recent observations.

```python
# By span (approximate rolling window)
df['ewm'] = df['value'].ewm(span=7).mean()

# By alpha (smoothing factor, 0-1)
df['ewm'] = df['value'].ewm(alpha=0.3).mean()

# By halflife
df['ewm'] = df['value'].ewm(halflife='7 days').mean()
```

**Rule of thumb:** span = (2/alpha) - 1

---

## Shifting and Differencing

### Shift (Lag/Lead)

```python
# Lag (previous values)
df['prev_day'] = df['value'].shift(1)
df['prev_week'] = df['value'].shift(7)

# Lead (future values)
df['next_day'] = df['value'].shift(-1)

# Calculate returns
df['returns'] = (df['price'] - df['price'].shift(1)) / df['price'].shift(1)
df['returns'] = df['price'].pct_change()  # Same thing
```

### Difference

```python
# First difference
df['diff'] = df['value'].diff()

# Second difference
df['diff2'] = df['value'].diff().diff()

# Percentage change
df['pct_change'] = df['value'].pct_change()
```

---

## Timezone Handling

### Localize (Add Timezone)

```python
# Naive datetime to timezone-aware
df.index = df.index.tz_localize('UTC')
df.index = df.index.tz_localize('America/New_York')

# Handle ambiguous times (DST)
df.index = df.index.tz_localize('America/New_York', ambiguous='infer')
```

### Convert Between Timezones

```python
# Convert from one timezone to another
df.index = df.index.tz_convert('America/Los_Angeles')

# UTC to local
df.index = df.index.tz_convert('America/New_York')
```

### Best Practice

Store and compute in UTC, convert to local only for display:

```python
# Store as UTC
df.to_parquet('data.parquet')  # Index preserved

# Convert for display
display_df = df.copy()
display_df.index = display_df.index.tz_convert('America/New_York')
```

---

## DateOffset

For calendar-aware date arithmetic:

```python
from pandas.tseries.offsets import MonthEnd, BDay, DateOffset

# Add business days
df['due_date'] = df['start'] + BDay(5)

# Add months (respects month end)
df['next_month'] = df['date'] + MonthEnd(1)

# Custom offset
df['custom'] = df['date'] + DateOffset(months=3, days=15)
```

### Common Offsets

| Offset | Meaning |
|--------|---------|
| `Day(n)` | n calendar days |
| `BDay(n)` | n business days |
| `Week(n)` | n weeks |
| `MonthEnd(n)` | n month ends |
| `MonthBegin(n)` | n month starts |
| `QuarterEnd(n)` | n quarter ends |
| `YearEnd(n)` | n year ends |

---

## Period and PeriodIndex

For data representing time spans (months, quarters):

```python
# Create period
p = pd.Period('2024-03', freq='M')  # March 2024

# PeriodIndex
idx = pd.period_range('2024-01', periods=12, freq='M')

# Convert DatetimeIndex to PeriodIndex
df.index = df.index.to_period('M')

# Convert back
df.index = df.index.to_timestamp()
```

---

## Common Patterns

### Year-over-Year Comparison

```python
# Calculate YoY change
df['yoy_change'] = df['value'].pct_change(periods=365)

# Or with proper year alignment
current = df.loc['2024']
previous = df.loc['2023']
previous.index = previous.index + pd.DateOffset(years=1)
comparison = current.join(previous, rsuffix='_prev')
```

### Missing Date Detection

```python
# Find gaps in time series
full_range = pd.date_range(df.index.min(), df.index.max(), freq='D')
missing = full_range.difference(df.index)
print(f"Missing dates: {missing}")
```

### Reindexing to Fill Gaps

```python
# Add missing dates
full_range = pd.date_range(df.index.min(), df.index.max(), freq='D')
df = df.reindex(full_range)

# Then fill
df = df.ffill()  # or interpolate()
```
