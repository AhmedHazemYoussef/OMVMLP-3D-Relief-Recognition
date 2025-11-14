import os
import numpy as np
import pandas as pd
import pyvista as pv
from PIL import Image

# Directories
input_dir = "input"
output_dir = "output"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Step 1: Read the labels CSV
print("Reading labels CSV...")

# Step 2: Get list of .ply files
ply_files = [f for f in os.listdir(input_dir) if f.endswith(".ply")]
if not ply_files:
    print("No .ply files found in the input directory!")
    exit()

# Extract file indices from filenames
file_indices = [os.path.splitext(f)[0] for f in ply_files]  # e.g., "1", "2"

# View configurations (6 views using PyVista view_vector)
views = {
    "top": (0, 0, 1),       # Looking down z-axis
    "bottom": (0, 0, -1),   # Looking up z-axis
    "lateral_1": (-90, 0, 1),  # Left view
    "lateral_2": (90, 0, 1),   # Right view
    "lateral_3": (0, 90, 1),   # Front view
    "lateral_4": (0, -90, 1)   # Back view
}

# Function to process files
def process_files(input_dir, output_dir, files):
    for filename in files:
        file_name = f"{filename}.ply"
        ply_path = os.path.join(input_dir, file_name)
        print(f"Processing file: {filename}...")

        # Create folder for this object
        folder_name = f"{filename}"
        object_dir = os.path.join(output_dir, folder_name)
        os.makedirs(object_dir, exist_ok=True)

        # Load with PyVista
        try:
            reader = pv.get_reader(ply_path)
            mesh = reader.read()
        except Exception as e:
            print(f"Failed to load {ply_path}: {e}")
            continue

        if not mesh.n_faces:
            print(f"Skipping {filename}: No faces found.")
            continue


        # Set up PyVista plotter
        plotter = pv.Plotter(off_screen=True)
        plotter.window_size = (512, 512)
        plotter.add_mesh(mesh)

        # Capture views
        for view_name, angles in views.items():
            plotter.view_vector((angles[0], angles[1], angles[2]))
            screenshot = plotter.screenshot(return_img=True)  # Returns numpy array
            output_path = os.path.join(object_dir, f"{view_name}.png")
            Image.fromarray(screenshot).save(output_path)
            print(f"Saved {output_path}")

        plotter.close()

# Process all files
process_files(input_dir, output_dir, file_indices)

print("Done!")