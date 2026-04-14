
import pandas as pd

DEBUG=True

def log(message):
    if DEBUG:
        print(message)

filename = "data/trends_20260414.json"
df = pd.read_json(filename)

# Print number of rows
log(f"Loaded {len(df)} stories from {filename}\n")

df.drop_duplicates(subset=["post_id"], inplace=True)

print(f"After removing duplicates: {len(df)}")

df.dropna(subset=["post_id", "title", "score"], inplace=True)
print(f"After removing nulls: {len(df)}")

df["score"] = pd.to_numeric(df["score"], errors="coerce") # Converting scores to numeric
df = df.dropna(subset=["score"]) # dropping rows with invalid scores
df["score"] = df["score"].astype(int) # converting the score column to integer

df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")

df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)
df["title"] = df["title"].str.strip()

print(f"\nNumber of rows after cleaning: {len(df)}")

filename = "data/trends_clean.csv"
print(f"Saved {len(df)} rows to {filename}")

df.to_csv(filename, index=False)

print(f"\nStories per category:")

counts = df["category"].value_counts()


for category, count in counts.items():
    print(f"   {category:<15}{count}")




