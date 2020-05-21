from os import path

import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from IPython.display import display

save_path = 'trash_recognizer_save_1.h5'

loaded_model = keras.models.load_model(save_path)

data_dir = tf.keras.utils.get_file(origin="https://github.com/Insecuredude/Project-D/raw/Guus/ImageScroller/trash_images_01.tar", fname="real_trash_images_unsorted_compressed", untar=True)
data_dir = pathlib.Path(data_dir)
train_dir = os.path.join(data_dir,'training')
validation_dir = os.path.join(data_dir, 'validation')

image_count_bottles_training = len(os.listdir(os.path.join(train_dir,'bottles')))
image_count_cans_training = len(os.listdir(os.path.join(train_dir,'cans')))
image_count_training = image_count_bottles_training + image_count_cans_training
image_count_bottles_validation = len(os.listdir(os.path.join(validation_dir,'bottles')))
image_count_cans_validation = len(os.listdir(os.path.join(validation_dir,'cans')))
image_count_validation = image_count_bottles_validation + image_count_cans_validation

print("[INFO] number of bottles in training: ", image_count_bottles_training)
print("[INFO] number of cans in training: ", image_count_cans_training)
print("[INFO] number of images in training: ", image_count_training)
print("[INFO] number of bottles in validation: ", image_count_bottles_validation)
print("[INFO] number of cans in validation: ", image_count_cans_validation)
print("[INFO] number of images in validation: ", image_count_validation)
