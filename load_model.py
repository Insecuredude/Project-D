from os import path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from IPython.display import display

save_path = 'trash_recognizer_save_1.h5'

loaded_model = keras.models.load_model(save_path)

TEST_IMAGES_DIR = 

image_path = path.join('real_trash_images_unsorted','IMG-20200515-WA0018.JPG')
test_image_np = np.array(Image.open(image_path))
display(Image.fromarray(test_image_np))