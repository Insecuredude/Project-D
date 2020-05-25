import os
import pathlib

import numpy as np
import random
import tensorflow as tf
from tensorflow import keras
from PIL import Image
from IPython.display import display
import matplotlib.pyplot as plt
import math

global CLASS_NAMES
AUTOTUNE = tf.data.experimental.AUTOTUNE
IMG_WIDTH = 224
IMG_HEIGHT = 224
BATCH_SIZE = 32

save_path = 'trash_recognizer_model'

def main():
    global save_path, CLASS_NAMES

    labels_path = tf.keras.utils.get_file(
        'labels.txt',
        'https://raw.githubusercontent.com/Insecuredude/Project-D/Guus/labels.txt')
    CLASS_NAMES = np.array(open(labels_path).read().splitlines())

    loaded_model = keras.models.load_model(save_path)
    print(list(loaded_model.signatures.keys()))

    data_dir = tf.keras.utils.get_file(origin="https://github.com/Insecuredude/Project-D/raw/Guus/real_trash_images_unsorted_compressed.tar", fname="real_trash_images_unsorted_compressed", untar=True)
    test_images_dir = pathlib.Path(data_dir)

    test_image_count = len(os.listdir(test_images_dir))
    print("[INFO] number of test images: ", test_image_count)

    test_ds = tf.data.Dataset.list_files(str(test_images_dir/'*'))
    for f in test_ds.take(5):
        print(f)

    # Set `num_parallel_calls` so multiple images are loaded/processed in parallel.
    test_ds = test_ds.map(process_path, num_parallel_calls=AUTOTUNE)

    test_ds = prepare_for_testing(test_ds)
    
    output = { 0: 'bottle', 1: 'can'}
    it = iter(test_ds)
    for i in range(3):
        batch = next(it)
        result = loaded_model(batch)
        decoded = []
        for r in result:
            r = tf.nn.relu(r)
            print('raw result ->', r)
            v = tf.get_static_value(r)
            decoded.append(output[int(v)])
        print("result:\n", decoded)
        show_batch(batch, decoded)

        

def decode_img(img):
    global IMG_WIDTH, IMG_HEIGHT
    img = tf.image.decode_jpeg(img, channels = 3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return tf.image.resize(img, [IMG_WIDTH,  IMG_HEIGHT])

def process_path(file_path):
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img

def prepare_for_testing(ds, cache=True, shuffle_buffer_size=1000):
    global AUTOTUNE, BATCH_SIZE
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

def show_batch(image_batch, results):
    global CLASS_NAMES
    plt.figure(figsize=(10,10))
    for n in range(25):
        ax = plt.subplot(5,5,n+1)
        plt.imshow(image_batch[n])
        plt.title(str(results[n]))
        plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()