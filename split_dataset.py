import os
import shutil
import random

# ORIGINAL DATASET
SOURCE_DIR = "original_dataset/Garbage classification"

# NEW DATASET
DEST_DIR = "garbage_dataset"

# Split percentages
TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Keep the same random split every time
random.seed(42)

# Image file types
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# Create train, validation and test folders
for split in ["train", "validation", "test"]:
    os.makedirs(os.path.join(DEST_DIR, split), exist_ok=True)

# Process each class
for class_name in os.listdir(SOURCE_DIR):

    class_path = os.path.join(SOURCE_DIR, class_name)

    # Skip anything that isn't a folder
    if not os.path.isdir(class_path):
        continue

    # Get all images
    images = [
        file for file in os.listdir(class_path)
        if file.lower().endswith(IMAGE_EXTENSIONS)
    ]

    # Shuffle images
    random.shuffle(images)

    total = len(images)

    # Calculate split points
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VAL_RATIO)

    train_images = images[:train_end]
    validation_images = images[train_end:val_end]
    test_images = images[val_end:]

    # Create folders for this class
    for split in ["train", "validation", "test"]:
        os.makedirs(
            os.path.join(DEST_DIR, split, class_name),
            exist_ok=True
        )

    # Copy training images
    for image in train_images:
        shutil.copy2(
            os.path.join(class_path, image),
            os.path.join(DEST_DIR, "train", class_name, image)
        )

    # Copy validation images
    for image in validation_images:
        shutil.copy2(
            os.path.join(class_path, image),
            os.path.join(DEST_DIR, "validation", class_name, image)
        )

    # Copy testing images
    for image in test_images:
        shutil.copy2(
            os.path.join(class_path, image),
            os.path.join(DEST_DIR, "test", class_name, image)
        )

    print(
        f"{class_name}: "
        f"{len(train_images)} train, "
        f"{len(validation_images)} validation, "
        f"{len(test_images)} test"
    )

print("\nDataset splitting completed!")

