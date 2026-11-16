
import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from PIL import Image
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "garbage_dataset"
OUTPUT_DIR = BASE_DIR / "regression_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Existing category scores from features.py
SCORES = {
    "cardboard": 90,
    "glass": 95,
    "metal": 95,
    "paper": 90,
    "plastic": 70,
    "trash": 10
}


# Extract numerical features from an image
def extract_features(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        img = img.convert("RGB").resize((64, 64))

        pixels = np.array(img, dtype=np.float32)

        return {
            "mean_red": pixels[:, :, 0].mean(),
            "mean_green": pixels[:, :, 1].mean(),
            "mean_blue": pixels[:, :, 2].mean(),
            "brightness": pixels.mean(),
            "contrast": pixels.std(),
            "width": width,
            "height": height,
            "aspect_ratio": width / height if height else 0
        }


# Prepare dataset from image folders
def prepare_data(split):
    records = []

    for category, score in SCORES.items():
        folder = DATASET_DIR / split / category

        for image_path in folder.iterdir():
            if image_path.suffix.lower() not in [
                ".jpg", ".jpeg", ".png", ".webp", ".bmp"
            ]:
                continue

            try:
                features = extract_features(image_path)
                features["category"] = category
                features["recyclability_score"] = score
                records.append(features)
            except Exception as error:
                print("Skipping:", image_path.name, error)

    return pd.DataFrame(records)


print("Preparing training data...")
train_data = prepare_data("train")

print("Preparing testing data...")
test_data = prepare_data("test")

if train_data.empty or test_data.empty:
    raise ValueError("No images found. Check your dataset folders.")

# Save extracted numerical data
train_data.to_csv(OUTPUT_DIR / "train_features.csv", index=False)
test_data.to_csv(OUTPUT_DIR / "test_features.csv", index=False)

# Select input features and target
# Use waste category as a categorical input
X_train = pd.get_dummies(
    train_data["category"], dtype=int
)

X_test = pd.get_dummies(
    test_data["category"], dtype=int
)

# Keep identical columns in training and testing
X_test = X_test.reindex(
    columns=X_train.columns, fill_value=0
)

y_train = train_data["recyclability_score"]
y_test = test_data["recyclability_score"]

# Train Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

# Predict scores
predictions = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, predictions)

print("\n--- REGRESSION RESULTS ---")
print("Training images:", len(X_train))
print("Testing images:", len(X_test))
print("MAE:", round(mae, 2))
print("MSE:", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4))

# Save model
joblib.dump(model, OUTPUT_DIR / "recyclability_model.pkl")

# Save actual vs predicted graph
plt.figure(figsize=(8, 6))
plt.scatter(y_test, predictions, alpha=0.6)
plt.plot([0, 100], [0, 100], "r--")
plt.xlabel("Actual Recyclability Score")
plt.ylabel("Predicted Recyclability Score")
plt.title("Actual vs Predicted - Linear Regression")
plt.savefig(OUTPUT_DIR / "actual_vs_predicted.png")
plt.close()

print("\nModel, datasets and graph saved in regression_outputs!")

