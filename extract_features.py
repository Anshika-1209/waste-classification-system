import os
import cv2
import numpy as np
import pandas as pd

# Correct path based on your folder structure screenshot
DATASET_PATH = "garbage_dataset/train" 

# Exact lowercase folder names from your screenshot
CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]

data = []

print("Starting feature extraction...")

for class_name in CLASSES:
    class_folder = os.path.join(DATASET_PATH, class_name)
    
    if not os.path.exists(class_folder):
        print(f"Warning: Folder not found -> {class_folder}")
        continue
        
    for filename in os.listdir(class_folder):
        img_path = os.path.join(class_folder, filename)
        
        img = cv2.imread(img_path)
        if img is None:
            continue
            
        height, width, _ = img.shape
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        r_mean = np.mean(img_rgb[:, :, 0])
        g_mean = np.mean(img_rgb[:, :, 1])
        b_mean = np.mean(img_rgb[:, :, 2])
        brightness = 0.299 * r_mean + 0.587 * g_mean + 0.114 * b_mean
        
        data.append({
            "filename": filename,
            "class": class_name,
            "width": width,
            "height": height,
            "red_mean": round(r_mean, 2),
            "green_mean": round(g_mean, 2),
            "blue_mean": round(b_mean, 2),
            "brightness": round(brightness, 2)
        })

df = pd.DataFrame(data)
df.to_csv("waste_features.csv", index=False)
print(f"Feature extraction complete! Saved {len(df)} records to waste_features.csv")
