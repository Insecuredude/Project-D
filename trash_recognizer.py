import tensorflow as tf
AUTOTUNE = tf.data.experimental.AUTOTUNE
import IPython.display as display
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import pathlib
import time

def main():
    print("first test")
    data_dir = tf.keras.utils.get_file(origin="/ImageScroller/trash_images.tar", fname="/ImageScroller/trash_images.tar", untar=True)
    data_dir = pathlib.Path(data_dir)

if __name__ == '__main__':
    main()