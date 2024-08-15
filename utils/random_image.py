import os
from random import choice


def get_random_image():
    image_folder = os.path.join(os.path.dirname(__file__), 'pet_images')
    images = os.listdir(image_folder)
    random_image = choice(images)
    return os.path.join(image_folder, random_image)
