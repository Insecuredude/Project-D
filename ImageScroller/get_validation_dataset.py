#!/usr/bin/python3.8 -tt
import os
from os import listdir
from os.path import join
import math
import random

import argparse

def MoveImages(per = 0.2):
    train_dir = os.path.join('trash_images_01','training')
    validation_dir = os.path.join('trash_images_01','validation')

    bottles_training = os.listdir(os.path.join(train_dir,'bottles'))
    cans_training = os.listdir(os.path.join(train_dir,'cans'))

    image_count_bottles_training = len(bottles_training)
    image_count_cans_training = len(cans_training)
    image_count_training = image_count_bottles_training + image_count_cans_training

    print("[INFO] percentage:", per * 100,'%')
    print("[INFO] number of bottles in training: ", image_count_bottles_training)
    print("[INFO] number of cans in training: ", image_count_cans_training)
    print("[INFO] number of images in training: ", image_count_training)
    print()

    image_count_bottles_tomove = math.floor(image_count_bottles_training * per)
    image_count_cans_tomove = math.floor(image_count_cans_training * per)
    image_count_tomove = math.floor(image_count_training * per)

    print("[INFO] number of bottles to move: ", image_count_bottles_tomove)
    print("[INFO] number of cans to move: ", image_count_cans_tomove)
    print("[INFO] number of images to move: ", image_count_tomove)
    print()

    bottles_tomove = random.sample(bottles_training, image_count_bottles_tomove)
    cans_tomove = random.sample(cans_training, image_count_cans_tomove)
    
    bottles_moved = 0
    for bottle in bottles_tomove:
        bottle_dir = os.path.join(train_dir,'bottles',bottle)
        dst = os.path.join(validation_dir,'bottles',bottle)
        os.replace(bottle_dir, dst)
        bottles_moved = bottles_moved + 1

    
    cans_moved = 0
    for can in cans_tomove:
        can_dir = os.path.join(train_dir,'cans',can)
        dst = os.path.join(validation_dir,'cans',can)
        os.replace(can_dir, dst)
        cans_moved = cans_moved + 1

    print("[INFO] number of bottles moved: ", bottles_moved)
    print("[INFO] number of cans moved: ", cans_moved)
    print()

    

#Define a main() function that prints a litte greeting
def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--per", required=False,
        help="percentage of images you want to move from the dataset to the validation dataset (0.0 - 1.0)")
    args = vars(ap.parse_args())
    if args["per"]:
        MoveImages(args["per"])
    else:
        MoveImages()

# This is the standard boilerplate that calls the maun function.
if __name__ == '__main__':
    main()