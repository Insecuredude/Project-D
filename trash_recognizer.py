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
EPOCHS = 10
default_timeit_steps = 1000

def main():
    global IMG_HEIGHT,IMG_WIDTH, EPOCHS

    train_ds, validation_ds, image_count_training, image_count_validation = get_dataset()

    sample_training_images, _ = next(train_ds)

    show_batch(sample_training_images[:5])

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

    history = model.fit_generator(
        train_ds,
        steps_per_epoch= image_count_training,
        epochs= EPOCHS,
        validation_data= validation_ds,
        validation_steps= image_count_validation
    )

    visualize_history(history)

def get_dataset():
    global CLASS_NAMES, BATCH_SIZE, IMG_HEIGHT, IMG_WIDTH
    #Downloading the dataset from github
    data_dir = tf.keras.utils.get_file(origin="https://github.com/Insecuredude/Project-D/raw/Guus/ImageScroller/trash_images_01.tar", fname="trash_images_01", untar=True)
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

    train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
    validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

    train_data_gen = train_image_generator.flow_from_directory(batch_size=BATCH_SIZE,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')

    val_data_gen = validation_image_generator.flow_from_directory(batch_size=BATCH_SIZE,
                                                              directory=validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')
    
    return train_data_gen, val_data_gen, image_count_training, image_count_validation

def show_batch(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_history(history):
    global EPOCHS

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss=history.history['loss']
    val_loss=history.history['val_loss']

    epochs_range = range(EPOCHS)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()


if __name__ == '__main__':
    main()