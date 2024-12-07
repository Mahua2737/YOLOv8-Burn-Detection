import os
import shutil


source_images = "E:\python\VisionHack_CV_ETE\CV_ETE"
source_labels = "E:\python\VisionHack_CV_ETE\CV_ETE"

# dataset structure
dataset_dir = "dataset"
train_images_dir = os.path.join(dataset_dir, "train/images")
train_labels_dir = os.path.join(dataset_dir, "train/labels")
val_images_dir = os.path.join(dataset_dir, "val/images")
val_labels_dir = os.path.join(dataset_dir, "val/labels")

# Create directories
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Split dataset (80% train, 20% val)
image_files = [f for f in os.listdir(source_images) if f.endswith(".jpg")]
label_files = [f.replace(".jpg", ".txt") for f in image_files]

split_ratio = 0.8
split_index = int(len(image_files) * split_ratio)

train_images = image_files[:split_index]
val_images = image_files[split_index:]

# Move training files
for image_file in train_images:
    shutil.copy(os.path.join(source_images, image_file), train_images_dir)
    label_file = image_file.replace(".jpg", ".txt")
    shutil.copy(os.path.join(source_labels, label_file), train_labels_dir)

# Move validation files
for image_file in val_images:
    shutil.copy(os.path.join(source_images, image_file), val_images_dir)
    label_file = image_file.replace(".jpg", ".txt")
    shutil.copy(os.path.join(source_labels, label_file), val_labels_dir)

print("Dataset organized successfully!")
