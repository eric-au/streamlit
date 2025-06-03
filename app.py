import streamlit as st
import pandas as pd
import altair as alt

st.title("Hello, World! 👋")
st.write("Welcome to your first Streamlit app.")

# -- Load data --------------------------------------------------
@st.cache_data
def load_data(path_or_file):
    return pd.read_csv(path_or_file)

data_source = st.sidebar.radio(
    "Choose data source",
    ("Repo CSV", "Upload your own")
)

if data_source == "Repo CSV":
    df = load_data("https://github.com/eric-au/streamlit/blob/main/sales_data_sample.csv")   # path inside your repo
else:
    uploaded = st.file_uploader("Upload a CSV", type="csv")
    if uploaded:
        df = load_data(uploaded)
    else:
        st.stop()
      
# -- Basic profile ---------------------------------------------
st.subheader("Preview")
st.dataframe(df, use_container_width=True)

with st.expander("Quick stats"):
    st.write(df.describe(include="all").transpose())

# -- Simple interactive filter ---------------------------------
st.sidebar.markdown("### Filters")
col = st.sidebar.selectbox("Column to filter", df.columns)
if pd.api.types.is_numeric_dtype(df[col]):
    min_val, max_val = st.sidebar.slider(
        "Range", float(df[col].min()), float(df[col].max()),
        (float(df[col].min()), float(df[col].max()))
    )
    df = df[df[col].between(min_val, max_val)]
else:
    choices = st.sidebar.multiselect(
        "Values", df[col].unique(), default=list(df[col].unique())
    )
    df = df[df[col].isin(choices)]

st.write(f"Filtered rows: {len(df)}")

# -- Example chart ---------------------------------------------
chart_type = st.radio("Chart", ["Bar", "Line", "Area"], horizontal=True)
if chart_type == "Bar":
    chart = alt.Chart(df).mark_bar().encode(x=col, y='count()')
elif chart_type == "Line":
    chart = alt.Chart(df).mark_line().encode(x=col, y='count()')
else:
    chart = alt.Chart(df).mark_area().encode(x=col, y='count()')
st.altair_chart(chart, use_container_width=True)

# -- Let users edit & download ---------------------------------
edited = st.data_editor(df, key="editor")   # Streamlit ≥ 1.29
st.download_button("Download current view",
                   edited.to_csv(index=False),
                   "filtered.csv")
