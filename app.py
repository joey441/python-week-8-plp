import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the trimmed dataset
try:
    df = pd.read_csv('trimmed_metadata.csv')
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df.dropna(subset=['publish_time'], inplace=True)
    df['year'] = df['publish_time'].dt.year
    df['journal'].fillna('Unknown', inplace=True)
except FileNotFoundError:
    st.error("Trimmed dataset not found. Please run the data loading script first.")
    st.stop()

# --- Streamlit App Layout ---
st.title("CORD-19 Data Explorer 🔬")
st.write("A simple exploration of COVID-19 research papers using a trimmed subset of the CORD-19 dataset.")

# Sidebar for interactive controls
st.sidebar.header("Filter Options")

# Slider for year range
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df['year'].min()),
    int(df['year'].max()),
    (2020, 2021)
)

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# --- Display Sections ---
st.header("Publications Over Time")
st.write(f"Showing data for the years **{year_range[0]}** to **{year_range[1]}**.")
publications_by_year = filtered_df['year'].value_counts().sort_index()

fig, ax = plt.subplots()
sns.lineplot(x=publications_by_year.index, y=publications_by_year.values, marker='o', ax=ax)
ax.set_title('Number of Publications by Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
st.pyplot(fig)

st.header("Top 10 Publishing Journals")
top_journals = filtered_df['journal'].value_counts().nlargest(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis', ax=ax)
ax.set_title(f'Top 10 Publishing Journals ({year_range[0]}-{year_range[1]})')
ax.set_xlabel('Number of Papers')
ax.set_ylabel('Journal')
st.pyplot(fig)

st.header("Sample Data")
st.write("A small sample of the filtered dataset:")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year']].head(10))
