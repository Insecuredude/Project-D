import tensorflow as tf
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
    global CLASS_NAMES

    data_dir = tf.keras.utils.get_file(origin="https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz",fname="flower_photos",untar=True)
    data_dir = pathlib.Path(data_dir)

    image_count = len(list(data_dir.glob('*/*.jpg')))
    print("image count: ",image_count)

    CLASS_NAMES = np.array([item.name for item in data_dir.glob('*') if item.name != "LICENSE.txt"])
    print("class names: ", CLASS_NAMES)

    list_ds = tf.data.Dataset.list_files(str(data_dir/'*/*'))
    labeled_ds = list_ds.map(process_path, num_parallel_calls=AUTOTUNE)

    train_ds = prepare_for_training(labeled_ds)

    image_batch, label_batch = next(iter(train_ds))

    #show_batch(image_batch.numpy(), label_batch.numpy())
    timeit(train_ds)




def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2] == CLASS_NAMES

def decode_img(img):
    global IMG_WIDTH, IMG_HEIGHT
    img = tf.image.decode_jpeg(img, channels = 3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    return tf.image.resize(img, [IMG_WIDTH,IMG_HEIGHT])

def process_path(file_path):
    label = get_label(file_path)
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    return img,label

def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
    global BATCH_SIZE

    if cache:
        if isinstance(cache, str):
            ds = ds.cache(cache)
        else:
            ds = ds.cache()
    
    ds = ds.shuffle(buffer_size = shuffle_buffer_size)

    ds = ds.repeat()

    ds = ds.batch(BATCH_SIZE)

    ds = ds.prefetch(buffer_size = AUTOTUNE)

    return ds

def show_batch(image_batch, label_batch):
    plt.figure(figsize=(10,10))
    for n in range(25):
        plt.subplot(5,5,n+1)
        plt.imshow(image_batch[n])
        plt.title(CLASS_NAMES[label_batch[n]==1][0].title())
        plt.axis('off')
    plt.show()

def timeit(ds, steps=default_timeit_steps):
    global BATCH_SIZE

    start = time.time()
    it = iter(ds)
    for i in range(steps):
        batch = next(it)
        if i%10 == 0:
            print('.',end='')
    print()
    end = time.time()

    duration = end-start
    print("{} batches: {} s".format(steps, duration))
    print("{:0.5f} Images/s".format(BATCH_SIZE*steps/duration))

if __name__ == '__main__':
    main()