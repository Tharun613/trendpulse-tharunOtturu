import pandas as pd
import os
import matplotlib.pyplot as plt

## 1 -- Setup 
filename = "data/trends_analysed.csv"
df = pd.read_csv(filename)

os.makedirs("outputs", exist_ok=True)

def display_chart(path):
    plt.savefig(path)
    plt.show()

def add_labels_titles(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

## Chart 1: Top 10 Stories by Score

top_stories = df.sort_values(by="score", ascending=False).head(10)

top_stories['short_title'] =  top_stories['title'].str[:50]

plt.figure()

plt.barh(top_stories["short_title"], top_stories["score"])

add_labels_titles("Score", "Story Title", "Top 10 Stories by Score")

plt.gca().invert_yaxis()

display_chart("outputs/chart1_top_stories.png")


## Chart 2: Stories per Category

counts = df["category"].value_counts()

colors = ["violet", "cyan", "green", "orange", "purple"]

plt.figure()

plt.bar(counts.index, counts.values, color=colors)

add_labels_titles("Category", "Number of Stories", "Number of Stories per Category")

display_chart("outputs/chart2_categories.png")


## Chart 3: Score vs Comments

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

add_labels_titles("Score", "Number of Comments", "Score vs Comments")

plt.legend()

display_chart("outputs/chart3_scatter.png")


## Bonus: Dashboard

fig, axes = plt.subplots(1, 3, figsize=(18,5))


axes[0].barh(top_stories["short_title"], top_stories["score"])
axes[0].invert_yaxis()
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")


axes[1].bar(counts.index, counts.values, color=colors)
axes[1].set_title("Number of Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")

axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number ofComments")
axes[2].legend()

# Overall title
plt.suptitle("TrendPulse Dashboard")

display_chart("outputs/dashboard.png")