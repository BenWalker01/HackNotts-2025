from PIL import Image
import os
import sys


def extract_frames(path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(path)
    for frame in range(img.n_frames):
        img.seek(frame)
        frame_path = os.path.join(output_dir, f"frame_{frame}.png")
        img.save(frame_path, format="PNG")


if __name__ == "__main__":
    path = sys.argv[1]
    extract_frames(path, "assets/character/models/sequences")
