# Streamlit API Reference

Complete API documentation organized by category.

## Write and Magic

### st.write()

Universal output function - displays text, data, charts, and more.

```python
st.write("Hello **world**!")  # Markdown text
st.write(df)                   # DataFrame
st.write(fig)                  # Matplotlib figure
st.write(1234)                 # Numbers
st.write({"a": 1, "b": 2})     # Dicts
```

### st.write_stream()

Display streaming data with typewriter effect:

```python
st.write_stream(my_generator)
st.write_stream(llm_response_stream)
```

### Magic Commands

Variables alone on a line auto-display:

```python
"Hello **world**!"  # Displays as markdown
df                  # Displays dataframe
fig                 # Displays figure
```

---

## Text Elements

| Function | Purpose | Example |
|----------|---------|---------|
| `st.title()` | Largest heading | `st.title("App Title")` |
| `st.header()` | Section heading | `st.header("Section")` |
| `st.subheader()` | Subsection | `st.subheader("Details")` |
| `st.markdown()` | Markdown text | `st.markdown("**bold**")` |
| `st.text()` | Monospace text | `st.text("Fixed width")` |
| `st.caption()` | Small caption | `st.caption("Note")` |
| `st.code()` | Code block | `st.code("x = 1", language="python")` |
| `st.latex()` | LaTeX math | `st.latex(r"\int x^2 dx")` |
| `st.divider()` | Horizontal line | `st.divider()` |
| `st.html()` | Raw HTML | `st.html("<b>Bold</b>")` |

---

## Data Elements

### st.dataframe()

Interactive table with sorting, filtering, selection:

```python
st.dataframe(df)

# With configuration
st.dataframe(
    df,
    column_config={
        "price": st.column_config.NumberColumn("Price", format="$%.2f"),
        "url": st.column_config.LinkColumn("Link"),
    },
    hide_index=True,
    use_container_width=True,
)

# With selection
event = st.dataframe(df, on_select="rerun", selection_mode="multi-row")
selected_rows = event.selection.rows
```

### st.data_editor()

Editable dataframe:

```python
edited_df = st.data_editor(df)
edited_df = st.data_editor(df, num_rows="dynamic")  # Allow adding rows
```

### st.table()

Static table (no interactivity):

```python
st.table(df)
```

### st.metric()

KPI display with delta:

```python
st.metric("Revenue", "$1,234", "+12%")
st.metric("Temperature", "72F", "-5F", delta_color="inverse")
```

### st.json()

Pretty-printed JSON:

```python
st.json({"key": "value", "nested": {"a": 1}})
```

### Column Configuration

```python
st.column_config.TextColumn("Name")
st.column_config.NumberColumn("Price", format="$%.2f", min_value=0)
st.column_config.CheckboxColumn("Active")
st.column_config.SelectboxColumn("Status", options=["Open", "Closed"])
st.column_config.DateColumn("Date")
st.column_config.TimeColumn("Time")
st.column_config.DatetimeColumn("Timestamp")
st.column_config.LinkColumn("URL")
st.column_config.ImageColumn("Photo")
st.column_config.ProgressColumn("Progress", min_value=0, max_value=100)
st.column_config.BarChartColumn("Values")
st.column_config.LineChartColumn("Trend")
```

---

## Chart Elements

### Simple Charts

All accept DataFrame or array-like data:

```python
st.line_chart(df)
st.line_chart(df, x="date", y=["sales", "revenue"], color="category")

st.bar_chart(df)
st.area_chart(df)
st.scatter_chart(df, x="x", y="y", size="magnitude", color="type")
```

### Map

Requires columns named `lat`/`latitude` and `lon`/`longitude`:

```python
st.map(df)
st.map(df, latitude="lat", longitude="lon", size="population")
```

### External Libraries

```python
# Matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
st.pyplot(fig)

# Plotly
import plotly.express as px
fig = px.scatter(df, x="x", y="y", color="category")
st.plotly_chart(fig, use_container_width=True)

# Altair
import altair as alt
chart = alt.Chart(df).mark_circle().encode(x="x", y="y", color="category")
st.altair_chart(chart, use_container_width=True)

# Bokeh
st.bokeh_chart(bokeh_figure)

# PyDeck
st.pydeck_chart(deck_gl_chart)

# Graphviz
st.graphviz_chart("digraph { A -> B -> C }")
```

---

## Input Widgets

### Buttons

```python
# Basic button
if st.button("Click me"):
    st.write("Clicked!")

# Styled button
st.button("Primary", type="primary")
st.button("Secondary", type="secondary")

# With icon
st.button("Save", icon=":material/save:")

# With keyboard shortcut
st.button("Submit", shortcut="Ctrl+Enter")

# Link button (opens URL)
st.link_button("Go to Streamlit", "https://streamlit.io")

# Download button
st.download_button("Download CSV", csv_data, "data.csv", "text/csv")
```

### Text Input

```python
# Single line
name = st.text_input("Name", placeholder="Enter your name")
password = st.text_input("Password", type="password")

# Multi-line
bio = st.text_area("Bio", height=200)

# With validation via callback
def validate():
    if len(st.session_state.email) < 5:
        st.error("Too short")

st.text_input("Email", key="email", on_change=validate)
```

### Numeric Input

```python
age = st.number_input("Age", min_value=0, max_value=120, value=25, step=1)
price = st.number_input("Price", min_value=0.0, format="%.2f")
```

### Selection

```python
# Single select
option = st.selectbox("Choose", ["A", "B", "C"])
option = st.selectbox("Choose", options, index=None, placeholder="Select...")

# Multiple select
selected = st.multiselect("Select multiple", ["A", "B", "C"], default=["A"])
selected = st.multiselect("Select", options, max_selections=3)

# Radio buttons
choice = st.radio("Pick one", ["Option 1", "Option 2"], horizontal=True)
```

### Slider

```python
# Single value
value = st.slider("Value", 0, 100, 50)

# Range (pass tuple as value)
range_values = st.slider("Range", 0.0, 100.0, (25.0, 75.0))

# With step
value = st.slider("Value", 0, 100, 50, step=5)

# Select slider (discrete values)
size = st.select_slider("Size", options=["S", "M", "L", "XL"])
```

### Toggle/Checkbox

```python
show = st.checkbox("Show details")
if show:
    st.write("Details here")

enabled = st.toggle("Enable feature")
```

### File Upload

```python
# Single file
file = st.file_uploader("Upload file")
if file:
    df = pd.read_csv(file)

# Multiple files
files = st.file_uploader("Upload files", accept_multiple_files=True)

# Restrict types
image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
```

### Date/Time

```python
date = st.date_input("Select date")
date_range = st.date_input("Date range", value=(start, end))

time = st.time_input("Select time")

color = st.color_picker("Pick a color", "#00ff00")
```

### Camera/Audio

```python
photo = st.camera_input("Take a photo")
audio = st.audio_input("Record audio")
```

---

## Layout and Containers

### Sidebar

```python
st.sidebar.title("Settings")
option = st.sidebar.selectbox("Choose", options)
st.sidebar.slider("Value", 0, 100)

# Or with context manager
with st.sidebar:
    st.title("Settings")
    option = st.selectbox("Choose", options)
```

### Columns

```python
# Equal columns
col1, col2, col3 = st.columns(3)
col1.write("Column 1")
col2.write("Column 2")
col3.write("Column 3")

# Unequal columns (ratios)
left, right = st.columns([2, 1])

# With gap
col1, col2 = st.columns(2, gap="large")

# Using context manager
with col1:
    st.write("Left content")
```

### Tabs

```python
tab1, tab2, tab3 = st.tabs(["Data", "Charts", "Settings"])

with tab1:
    st.dataframe(df)

with tab2:
    st.line_chart(df)

with tab3:
    st.checkbox("Option")
```

### Expander

```python
with st.expander("Click to expand"):
    st.write("Hidden content")
    st.image("image.png")

# Initially expanded
with st.expander("Details", expanded=True):
    st.write("Visible by default")
```

### Container

```python
# Basic container
with st.container():
    st.write("Inside container")

# Out-of-order insertion
container = st.container()
st.write("This appears second")
container.write("This appears first")

# With border
with st.container(border=True):
    st.write("Bordered content")
```

### Empty (Placeholder)

```python
placeholder = st.empty()
placeholder.text("Loading...")
# Later...
placeholder.text("Done!")
# Or clear it
placeholder.empty()
```

### Popover

```python
with st.popover("Settings"):
    st.checkbox("Option 1")
    st.slider("Value", 0, 100)
```

### Dialog

```python
@st.dialog("Confirm")
def confirm_dialog():
    st.write("Are you sure?")
    if st.button("Yes"):
        st.session_state.confirmed = True
        st.rerun()

if st.button("Delete"):
    confirm_dialog()
```

---

## Chat Elements

### st.chat_message()

```python
with st.chat_message("user"):
    st.write("Hello!")

with st.chat_message("assistant"):
    st.write("How can I help?")

# Custom avatar
with st.chat_message("assistant", avatar="logo.png"):
    st.write("Response")
```

### st.chat_input()

```python
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"You said: {prompt}")
```

### Complete Chat Pattern

```python
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Handle new input
if prompt := st.chat_input("Message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = get_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
```

---

## Status Elements

### Messages

```python
st.success("Operation successful!")
st.info("This is informational")
st.warning("Be careful!")
st.error("Something went wrong")
st.exception(e)  # Display exception with traceback
```

### Progress

```python
# Progress bar
progress = st.progress(0)
for i in range(100):
    progress.progress(i + 1)

# With text
progress = st.progress(0, text="Processing...")
```

### Spinner

```python
with st.spinner("Loading..."):
    time.sleep(2)
st.success("Done!")
```

### Status Container

```python
with st.status("Running analysis...") as status:
    st.write("Loading data...")
    load_data()
    st.write("Processing...")
    process()
    status.update(label="Complete!", state="complete")
```

### Toast

```python
st.toast("File saved!")
st.toast("Warning: Low memory", icon="warning")
```

### Celebrations

```python
st.balloons()  # Balloon animation
st.snow()      # Snowfall animation
```

---

## Media Elements

```python
# Images
st.image("image.png")
st.image(numpy_array)
st.image("https://example.com/image.jpg")
st.image(image, caption="My Image", width=300)

# Audio
st.audio("audio.mp3")
st.audio(audio_bytes, format="audio/mp3")

# Video
st.video("video.mp4")
st.video("https://youtube.com/watch?v=xxx")

# Logo
st.logo("logo.png")
```

---

## Caching

### @st.cache_data

For serializable data (DataFrames, dicts, lists, strings):

```python
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

@st.cache_data(ttl=3600)  # Expire after 1 hour
def fetch_api():
    return requests.get(url).json()

@st.cache_data(max_entries=100)  # Limit cache size
def process(input):
    return expensive_computation(input)

@st.cache_data(show_spinner="Loading data...")
def load():
    return pd.read_csv("data.csv")

# Exclude unhashable parameters (prefix with _)
@st.cache_data
def query(_connection, sql):
    return _connection.execute(sql)
```

### @st.cache_resource

For singleton resources (DB connections, ML models):

```python
@st.cache_resource
def load_model():
    return SomeLargeModel()

@st.cache_resource
def init_db():
    return create_connection()
```

### Cache Control

```python
# Clear specific cache
load_data.clear()

# Clear all caches
st.cache_data.clear()
st.cache_resource.clear()
```

---

## Session State

```python
# Initialize
if "count" not in st.session_state:
    st.session_state.count = 0

# Read
value = st.session_state.count
value = st.session_state["count"]
value = st.session_state.get("count", 0)

# Write
st.session_state.count = 10
st.session_state["count"] = 10

# Delete
del st.session_state.count

# Check existence
if "count" in st.session_state:
    pass
```

### Widget-State Association

```python
# Widget value automatically syncs with session state
st.text_input("Name", key="user_name")
st.write(st.session_state.user_name)
```

### Callbacks

```python
def on_change():
    st.session_state.processed = process(st.session_state.input)

st.text_input("Input", key="input", on_change=on_change)

# With arguments
def update(value):
    st.session_state.total += value

st.button("Add 5", on_click=update, args=(5,))
st.button("Add 10", on_click=update, kwargs={"value": 10})
```

---

## Execution Flow

### Forms

```python
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"Hello {name}, age {age}")

# Clear on submit
with st.form("form", clear_on_submit=True):
    text = st.text_input("Message")
    st.form_submit_button("Send")
```

### Fragments

Partial reruns for isolated sections (v1.37+):

```python
@st.fragment
def filter_section():
    category = st.selectbox("Category", categories)
    filtered = data[data["category"] == category]
    st.dataframe(filtered)

# Main app
st.title("Dashboard")
expensive_chart()  # Only runs on full rerun
filter_section()   # Runs on its own interactions

# Auto-refresh fragment
@st.fragment(run_every="10s")
def live_data():
    st.write(get_latest())
```

### Control Flow

```python
st.stop()   # Stop script execution
st.rerun()  # Rerun from top

# Conditional stop
if not authenticated:
    st.error("Please log in")
    st.stop()
```

---

## Configuration

### st.set_page_config()

Must be the first Streamlit command:

```python
st.set_page_config(
    page_title="My App",
    page_icon=":chart:",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded",  # or "collapsed", "auto"
    menu_items={
        "Get Help": "https://example.com/help",
        "Report a Bug": "https://example.com/bug",
        "About": "My App v1.0"
    }
)
```

---

## Connections and Secrets

### st.connection()

```python
# SQL databases
conn = st.connection("my_db", type="sql")
df = conn.query("SELECT * FROM users", ttl="10m")

# Snowflake
conn = st.connection("snowflake")
df = conn.query("SELECT * FROM table")

# Session access
session = conn.session()
```

### st.secrets

Access `.streamlit/secrets.toml`:

```python
api_key = st.secrets["API_KEY"]
db_password = st.secrets["database"]["password"]

# Attribute access
api_key = st.secrets.API_KEY
```

**secrets.toml format:**

```toml
API_KEY = "sk-..."

[database]
host = "localhost"
password = "secret"

[connections.my_db]
dialect = "postgresql"
host = "localhost"
port = 5432
database = "mydb"
username = "user"
password = "secret"
```

---

## Authentication

```python
# Check login status
if not st.user.is_logged_in:
    st.button("Log in", on_click=st.login)
    st.stop()

# Access user info
st.write(f"Welcome, {st.user.name}")
st.write(st.user.email)

# Logout
st.button("Log out", on_click=st.logout)
```

Requires OIDC configuration in secrets.toml.

---

## Multipage Apps

### pages/ Directory Method

```
app.py
pages/
    1_Dashboard.py
    2_Analysis.py
    3_Settings.py
```

### st.navigation Method (v1.36+)

```python
import streamlit as st

dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
settings = st.Page("pages/settings.py", title="Settings")

pg = st.navigation([dashboard, settings])
pg.run()

# With sections
pg = st.navigation({
    "Main": [dashboard, analysis],
    "Admin": [settings, users],
})
```
