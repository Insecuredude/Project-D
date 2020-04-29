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
BATCH_SIZE = 32
default_timeit_steps = 1000


def main():
    global CLASS_NAMES, BATCH_SIZE

    data_dir = tf.keras.utils.get_file(origin="https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz",fname="flower_photos",untar=True)
    data_dir = pathlib.Path(data_dir)

    image_count = len(list(data_dir.glob('*/*.jpg')))
    print("image count: ",image_count)

    CLASS_NAMES = np.array([item.name for item in data_dir.glob('*') if item.name != "LICENSE.txt"])
    print("class names: ", CLASS_NAMES)

    #roses = list(data_dir.glob('roses/*'))

    #for image_path in roses[:3]:
    #    img = Image.open(str(image_path))
    #    img.show()

    image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    IMG_HEIGHT = 224
    IMG_WIDTH = 224
    STEPS_PER_EPOCH = np.ceil(image_count/BATCH_SIZE)

    train_data_gen = image_generator.flow_from_directory(directory=str(data_dir),
                                                        batch_size=BATCH_SIZE,
                                                        shuffle=True,
                                                        target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                        classes = list(CLASS_NAMES))

    image_batch, label_batch = next(train_data_gen)
    timeit(train_data_gen)

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