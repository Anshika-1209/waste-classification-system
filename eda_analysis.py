import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the extracted features CSV
df = pd.read_csv("waste_features.csv")

# Set style for graphs
sns.set_theme(style="whitegrid")

# 1. Class Distribution Count Plot
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="class", palette="viridis")
plt.title("Number of Images per Waste Class")
plt.xlabel("Waste Category")
plt.ylabel("Image Count")
plt.savefig("class_distribution.png")
plt.close()

# 2. Average Brightness per Waste Class (Boxplot)
plt.figure(figsize=(9, 5))
sns.boxplot(data=df, x="class", y="brightness", palette="Set2")
plt.title("Image Brightness Distribution Across Waste Categories")
plt.xlabel("Waste Category")
plt.ylabel("Brightness (Luminance)")
plt.savefig("brightness_boxplot.png")
plt.close()

# 3. Correlation Heatmap of Numerical Features
plt.figure(figsize=(7, 6))
numeric_cols = ["width", "height", "red_mean", "green_mean", "blue_mean", "brightness"]
correlation_matrix = df[numeric_cols].corr()

sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Image Features")
plt.savefig("correlation_heatmap.png")
plt.close()

print("EDA completed! Generated charts: class_distribution.png, brightness_boxplot.png, correlation_heatmap.png")
