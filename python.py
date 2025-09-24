# ==============================================================================
# Frameworks Assignment: CORD-19 Data Analysis
#
# This script performs data loading, cleaning, analysis, and visualization
# on a trimmed version of the CORD-19 metadata.csv file.
#
# Author: Your Name
# GitHub Repo: (Will be added later)
# ==============================================================================

# ==============================================================================
# Part 1: Data Loading and Basic Exploration
# ==============================================================================
import pandas as pd
import os

# Define the path to the trimmed dataset.
# The script assumes 'trimmed_metadata.csv' is in the same directory.
trimmed_file_path = 'trimmed_metadata.csv'

try:
    # Load the trimmed dataset
    df = pd.read_csv(trimmed_file_path)
    print("Successfully loaded the trimmed dataset.")
    
    # Basic exploration
    print("\n--- DataFrame Information ---")
    print(f"Shape of the dataset: {df.shape}")
    print("\nData types and missing values:")
    print(df.info())
    print("\nFirst 5 rows:")
    print(df.head())
    
except FileNotFoundError:
    print(f"Error: The file '{trimmed_file_path}' was not found.")
    print("Please ensure 'trimmed_metadata.csv' is in the same directory as this script.")
    exit()

# ==============================================================================
# Part 2: Data Cleaning and Preparation
# ==============================================================================
print("\n--- Starting Data Cleaning and Preparation ---")

# Create a cleaned version of the dataset to avoid modifying the original
df_cleaned = df.copy()

# Handle missing values in key columns
df_cleaned['abstract'].fillna('', inplace=True)
df_cleaned['title'].fillna('', inplace=True)
df_cleaned['journal'].fillna('Unknown', inplace=True)
df_cleaned['authors'].fillna('Unknown', inplace=True)

# Convert 'publish_time' to datetime format and drop rows where conversion fails
df_cleaned['publish_time'] = pd.to_datetime(df_cleaned['publish_time'], errors='coerce')
df_cleaned.dropna(subset=['publish_time'], inplace=True)

# Extract the year from the publication date
df_cleaned['year'] = df_cleaned['publish_time'].dt.year

# Create new columns for analysis
df_cleaned['abstract_word_count'] = df_cleaned['abstract'].apply(lambda x: len(x.split()))
print("Data cleaning and preparation complete. Ready for analysis.")
print(f"Cleaned DataFrame shape: {df_cleaned.shape}")

# ==============================================================================
# Part 3: Data Analysis and Visualization
# ==============================================================================
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud

print("\n--- Performing Data Analysis and Visualization ---")

# Set a consistent style for plots
sns.set_style("whitegrid")

# --- Analysis ---
# Count papers by publication year
publications_by_year = df_cleaned['year'].value_counts().sort_index()
print("\nTop 5 Years with the Most Publications:")
print(publications_by_year.head())

# Identify top journals publishing research
top_journals = df_cleaned['journal'].value_counts().nlargest(5)
print("\nTop 5 Publishing Journals:")
print(top_journals)

# --- Visualizations ---
# 1. Plot number of publications over time
plt.figure(figsize=(10, 6))
sns.lineplot(x=publications_by_year.index, y=publications_by_year.values, marker='o')
plt.title('Number of Publications Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.show()
print("Visualization 1: Publications over time plot generated.")

# 2. Bar chart of top publishing journals
plt.figure(figsize=(12, 8))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
plt.title('Top 5 Publishing Journals')
plt.xlabel('Number of Papers')
plt.ylabel('Journal')
plt.tight_layout()
plt.show()
print("Visualization 2: Top journals bar chart generated.")

# 3. Word cloud of paper titles
# To create the word cloud, we'll need to join all the titles into a single string
all_titles = ' '.join(df_cleaned['title'].tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Paper Titles')
plt.axis('off')
plt.show()
print("Visualization 3: Word cloud of paper titles generated.")


# ==============================================================================
# Part 5: Documentation
# ==============================================================================
print("\n--- Documentation and Reflection ---")
print("Remember to add comments to your code and create a README.md file for your GitHub repository.")
print("The README should summarize your findings and reflect on challenges and learnings.")

print("\nAssignment script execution complete.")