import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

AUTOTUNE = tf.data.experimental.AUTOTUNE
import IPython.display as display
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
import time

global CLASS_NAMES
IMG_WIDTH = 224
IMG_HEIGHT = 224
BATCH_SIZE = 32
default_timeit_steps = 1000

def main():
    global IMG_HEIGHT,IMG_WIDTH

    labeled_ds = get_dataset()
    for image, label in labeled_ds.take(1):
        print("Image shape: ", image.numpy().shape)
        print("Label: ", label.numpy())
    
    train_ds = prepare_for_training(labeled_ds)

    image_batch, label_batch = next(iter(train_ds))

    model = Sequential([
        Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
        MaxPooling2D(),
        Conv2D(32, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
    print(model.summary())


def get_dataset():
    global CLASS_NAMES
    #Downloading the dataset from github
    data_dir = tf.keras.utils.get_file(origin="https://github.com/Insecuredude/Project-D/raw/Guus/ImageScroller/trash_images.tar", fname="trash_images", untar=True)
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

    CLASS_NAMES = np.array([item for item in os.listdir(train_dir)])

    print("[INFO] labels: ",CLASS_NAMES)

    train_ds = tf.data.Dataset.list_files(os.path.join(train_dir,'*/*'))
    # Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
    labeled_training_ds = train_ds.map(process_path, num_parallel_calls=AUTOTUNE)

    return labeled_training_ds

def get_label(file_path):
    global CLASS_NAMES
    # convert the path to a list of path components
    parts = tf.strings.split(file_path, os.path.sep)
    # The second to last is the class-directory
    return parts[-2] == CLASS_NAMES

def decode_img(img):
    global IMG_WIDTH, IMG_HEIGHT
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [IMG_WIDTH, IMG_HEIGHT])

def process_path(file_path):
    label = get_label(file_path)
    # load the raw data from the file as a string
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img, label

def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
    global BATCH_SIZE
    # This is a small dataset, only load it once, and keep it in memory.
    # use `.cache(filename)` to cache preprocessing work for datasets that don't
    # fit in memory.
    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()

    ds = ds.shuffle(buffer_size=shuffle_buffer_size)

    # Repeat forever
    ds = ds.repeat()

    ds = ds.batch(BATCH_SIZE)

    # `prefetch` lets the dataset fetch batches in the background while the model
    # is training.
    ds = ds.prefetch(buffer_size=AUTOTUNE)

    return ds

def show_batch(image_batch, label_batch):
    plt.figure(figsize=(10,10))
    for n in range(25):
        plt.subplot(5,5,n+1)
        plt.imshow(image_batch[n])
        plt.title(CLASS_NAMES[label_batch[n]==1][0].title())
        plt.axis('off')
    plt.show()

if __name__ == '__main__':
    main()