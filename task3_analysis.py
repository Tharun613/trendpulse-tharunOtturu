# %%
import pandas as pd
import numpy as np

df = pd.read_csv("data/trends_clean.csv")

print(f"Loaded data: {df.shape}\n")

print(f"First 5 rows:")
print(df.head(5))

print(f"\nAverage score      : {np.round(df['score'].mean(), 0)}")
print(f"Average comments   : {np.round(df['num_comments'].mean(), 0)}\n")


np_scores = df['score'].values
average_score = np.round(np.mean(np_scores))

print("--- NumPy Stats ---")
print(f"Mean score    : {np.round(np.mean(np_scores))}")
print(f"Median score  : {np.round(np.median(np_scores))}")
print(f"Std deviation : {np.round(np.std(np_scores))}")
print(f"Max score     : {np.max(np_scores)}")
print(f"Min score     : {np.min(np_scores)}")

np_categories = df["category"].values
unique, counts = np.unique(np_categories, return_counts=True)

max_category = ""
max_count = 0
for category, count in zip(unique, counts):
    if count > max_count:
        max_category = category
        max_count = count

print(f"\nMost stories in: {max_category} ({max_count} stories)\n")

np_comments = df['num_comments'].values
max_index = np.argmax(np_comments)

story_with_most_comments = df.iloc[max_index]

print(f"Most commented story: \"{story_with_most_comments['title']}\" — {story_with_most_comments['num_comments']} comments")


df['engagement'] = np.round(df['num_comments']/ (df['score'] + 1), 2)

df['is_popular'] = df['score'] > average_score

filename = "data/trends_analysed.csv"
print(f"\nSaved to {filename}")
df.to_csv(filename, index=False)


