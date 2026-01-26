---
name: using-streamlit
description: Build interactive web applications with Streamlit. Use when creating data dashboards, chat/LLM apps, database-connected apps, or any Python web app that needs rapid prototyping. Covers execution model, caching, session state, widgets, and deployment.
---

# Using Streamlit

## Overview

Streamlit is a Python framework for building interactive web applications for data science and machine learning. It transforms Python scripts into shareable web apps with minimal effort, featuring automatic UI updates, built-in widgets, and seamless data visualization.

**Key Mental Model:** Streamlit reruns your entire script from top to bottom on every user interaction. This is the most important concept to understand.

## Quick Start

### Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install streamlit
streamlit hello  # Verify installation
```

### Minimal App

Create `app.py`:

```python
import streamlit as st

st.title("Hello Streamlit")
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")
```

Run with:

```bash
streamlit run app.py
```

## Core Concepts

### 1. Execution Model (Critical)

Every widget interaction triggers a complete script rerun. This means:

- Variables reset on each rerun unless stored in Session State
- Code runs top-to-bottom; order matters
- Expensive operations run repeatedly unless cached

```python
# This counter will ALWAYS show 1, never increment
count = 0
if st.button("Add"):
    count += 1  # Resets to 0 on next rerun
st.write(count)
```

### 2. Session State

Preserve data between reruns for each user session:

```python
import streamlit as st

# Initialize state (check first to avoid resetting)
if "count" not in st.session_state:
    st.session_state.count = 0

# Update state
if st.button("Add"):
    st.session_state.count += 1

st.write(f"Count: {st.session_state.count}")
```

**Widget-State Association:** Use `key` parameter to sync widget values with session state:

```python
st.slider("Temperature", 0.0, 100.0, key="temp")
st.write(st.session_state.temp)  # Access via key
```

### 3. Caching

Prevent expensive operations from running on every rerun.

**@st.cache_data** - For data (DataFrames, API responses, computations):

```python
@st.cache_data
def load_data(url):
    return pd.read_csv(url)  # Only loads once per URL

@st.cache_data(ttl=3600)  # Expire after 1 hour
def fetch_api_data():
    return requests.get(API_URL).json()
```

**@st.cache_resource** - For singleton resources (ML models, DB connections):

```python
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")  # Shared across all users

@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])
```

| Use Case | Decorator |
|----------|-----------|
| Load CSV/DataFrames | `@st.cache_data` |
| API calls | `@st.cache_data` |
| ML inference results | `@st.cache_data` |
| Load ML model | `@st.cache_resource` |
| Database connection | `@st.cache_resource` |

## Common Patterns

### Data Dashboard

```python
import streamlit as st
import pandas as pd

st.title("Data Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

data = load_data()

# Sidebar filters
st.sidebar.header("Filters")
category = st.sidebar.selectbox("Category", data["category"].unique())
min_value = st.sidebar.slider("Min Value", 0, 100, 25)

# Apply filters
filtered = data[(data["category"] == category) & (data["value"] >= min_value)]

# Display
col1, col2 = st.columns(2)
col1.metric("Total Records", len(filtered))
col2.metric("Average Value", f"{filtered['value'].mean():.2f}")

st.dataframe(filtered)
st.line_chart(filtered.set_index("date")["value"])
```

### Forms (Batch Input)

Forms prevent reruns until submit, useful for multi-field input:

```python
with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", 0, 120)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.success(f"Welcome {name}!")
    # Process form data here
```

### Chat/LLM App

```python
import streamlit as st
from openai import OpenAI

st.title("Chat App")

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle input
if prompt := st.chat_input("Message"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
```

### Multipage App

**Directory Structure:**

```
my_app/
    app.py           # Entry point
    pages/
        1_Dashboard.py
        2_Settings.py
        3_About.py
```

**Entry Point (app.py):**

```python
import streamlit as st

st.set_page_config(page_title="My App", layout="wide")
st.title("Welcome")
st.write("Select a page from the sidebar.")
```

Pages in `pages/` are auto-discovered. Number prefix controls order.

### Database Connection

```python
import streamlit as st

# Use st.connection for built-in connection management
conn = st.connection("my_db", type="sql")
df = conn.query("SELECT * FROM users WHERE active = true", ttl="10m")
st.dataframe(df)
```

**Secrets in `.streamlit/secrets.toml`:**

```toml
[connections.my_db]
dialect = "postgresql"
host = "localhost"
port = 5432
database = "mydb"
username = "user"
password = "secret"
```

## API Quick Reference

### Display

| Function | Purpose |
|----------|---------|
| `st.write()` | Universal output (text, data, charts) |
| `st.title()` / `st.header()` / `st.subheader()` | Headings |
| `st.markdown()` | Markdown text |
| `st.dataframe(df)` | Interactive table |
| `st.table(df)` | Static table |
| `st.metric("Label", value, delta)` | KPI display |
| `st.json(data)` | JSON viewer |

### Input Widgets

| Widget | Returns |
|--------|---------|
| `st.button("Click")` | `bool` (True on click) |
| `st.text_input("Label")` | `str` |
| `st.number_input("Label")` | `int` or `float` |
| `st.text_area("Label")` | `str` |
| `st.selectbox("Label", options)` | Selected option |
| `st.multiselect("Label", options)` | List of selected |
| `st.slider("Label", min, max)` | Number or tuple |
| `st.checkbox("Label")` | `bool` |
| `st.radio("Label", options)` | Selected option |
| `st.file_uploader("Label")` | UploadedFile or None |
| `st.date_input("Label")` | `date` |

### Layout

| Function | Purpose |
|----------|---------|
| `st.sidebar.write()` | Add to sidebar |
| `st.columns(n)` | Create n columns |
| `st.tabs(["Tab1", "Tab2"])` | Create tabs |
| `st.expander("Title")` | Collapsible section |
| `st.container()` | Grouping container |
| `st.empty()` | Replaceable placeholder |

### Charts

```python
st.line_chart(data)
st.bar_chart(data)
st.area_chart(data)
st.scatter_chart(data)
st.map(data)  # Requires lat/lon columns
st.pyplot(fig)  # Matplotlib
st.plotly_chart(fig)  # Plotly
st.altair_chart(chart)  # Altair
```

### Status

```python
st.success("Done!")
st.error("Failed!")
st.warning("Caution!")
st.info("Note:")
with st.spinner("Loading..."):
    do_work()
st.progress(50)  # 0-100
st.toast("Quick message")
```

## Pitfalls

### 1. Variables Reset on Every Rerun

**Wrong:**
```python
count = 0
if st.button("Add"):
    count += 1  # Always 1
```

**Correct:**
```python
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("Add"):
    st.session_state.count += 1
```

### 2. Missing Cache on Expensive Operations

**Wrong:**
```python
def load_data():
    return pd.read_csv("huge.csv")  # Reloads every interaction!
data = load_data()
```

**Correct:**
```python
@st.cache_data
def load_data():
    return pd.read_csv("huge.csv")
data = load_data()
```

### 3. Mutating Cached Resources

`@st.cache_resource` shares the same object instance across all users:

```python
@st.cache_resource
def get_list():
    return [1, 2, 3]

lst = get_list()
lst[0] = 999  # DANGER: Affects ALL users!
```

Use `@st.cache_data` for data you might modify.

### 4. Duplicate Widget IDs

```python
st.button("Submit")
st.button("Submit")  # ERROR: DuplicateWidgetID
```

**Fix:** Add unique keys:
```python
st.button("Submit", key="submit1")
st.button("Submit", key="submit2")
```

### 5. Accessing Uninitialized Session State

```python
value = st.session_state.my_key  # KeyError if not set!
```

**Fix:** Always check first:
```python
if "my_key" not in st.session_state:
    st.session_state.my_key = "default"
```

### 6. set_page_config Not First

```python
st.title("Hello")  # This runs first
st.set_page_config(page_title="App")  # ERROR!
```

`st.set_page_config()` must be the first Streamlit command.

### 7. Button Returns True Only Once

`st.button()` returns True only on the click event, then False:

```python
if st.button("Show"):
    st.write("Visible")  # Disappears after any other interaction
```

**Fix:** Use session state for persistent visibility:
```python
if st.button("Show"):
    st.session_state.show = True
if st.session_state.get("show"):
    st.write("Stays visible")
```

## Best Practices

1. **Always cache data loading** - Use `@st.cache_data` for DataFrames, API calls
2. **Initialize session state** - Check `if key not in st.session_state` before use
3. **Use forms for multi-field input** - Prevents partial submissions
4. **Use fragments for partial reruns** - `@st.fragment` for isolated sections
5. **Set TTL on cached data** - Prevent stale data: `@st.cache_data(ttl=3600)`
6. **Keep secrets in secrets.toml** - Never commit credentials; use `st.secrets`
7. **Use callbacks for widget updates** - `on_click`, `on_change` for reliable state
8. **Unique keys for dynamic widgets** - Especially in loops

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t myapp .
docker run -p 8501:8501 myapp
```

## Resources

See `references/api-reference.md` for the complete API documentation organized by category.

Full documentation available at https://docs.streamlit.io/
