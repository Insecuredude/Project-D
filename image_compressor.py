
################################################################################################
# name: image_compressor.py
# desc: Compress image file using python
# date: 2020-05-21
# Author: guusjoppe
# Based on: 05_compress_image_01.py from conquistadorjd
################################################################################################
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

print('*** Program Started ***')

image_path_input = '../Images/real_trash_images_unsorted/'
image_path_output = '../Images/real_trash_images_unsorted_compressed/'

images = os.listdir(image_path_input)
total_images = len(images)

cnt = 0
size_reductions = np.array([0])
for img in images:
    print(img)
    im = Image.open(image_path_input + img)
    img_size_before = os.path.getsize (image_path_input  + img)
    print('Input file size   : ', im.size )
    print('Input file name   : ', img )
    print('Input Image Size  : ', img_size_before)
    # image_name_output = '05_compress_image_01_output.png'
    image_name_output = img + '_compressed.jpg'

    im.save(image_path_output + image_name_output ,optimize=True,quality=50) 
    img_size_after = os.path.getsize (image_path_output + image_name_output)
    print('Output file size  : ', im.size )
    print('Output file name  : ', image_name_output)
    print('Output Image Size : ', img_size_after)
    
    size_reduction = 1 - img_size_after/img_size_before
    size_reductions = np.append(size_reductions, size_reduction)
    cnt = cnt + 1

print()
average_size_reduction = np.mean(size_reductions)
print(cnt,'/',total_images,'images compressed')
print('average size reduction: ', average_size_reduction)
print('*** Program Ended ***')