import os
from random import choice


def get_random_image() -> str:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_path = os.path.join(project_root, "pet_images")
    images = [f for f in os.listdir(images_path) if os.path.isfile(os.path.join(images_path, f))]
    return os.path.join(images_path, choice(images))
