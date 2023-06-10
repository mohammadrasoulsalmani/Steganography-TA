import sys
import math
from os import path

import cv2
import numpy as np

# Embed secret in the n least significant bit.
# Lower n make picture less loss but lesser storage capacity.
BITS = 2

HIGH_BITS = 256 - (1 << BITS)
LOW_BITS = (1 << BITS) - 1
BYTES_PER_BYTE = math.ceil(8 / BITS)
FLAG = '%'


def insert(img_path, msg):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)
    # Save origin shape to restore image
    ori_shape = img.shape
    print(ori_shape)
    max_bytes = ori_shape[0] * ori_shape[1] // BYTES_PER_BYTE
    # Encode message with length
    msg = '{}{}{}'.format(len(msg), FLAG, msg)
    # assert max_bytes >= len(
    #     msg), "Message greater than capacity:{}".format(max_bytes)
    if max_bytes <= len(msg):
        # Deficiency of pixels = Secret message bits - number of pixels
        Def_of_pixels = len(msg) - max_bytes 
        amount_of_increase_pixels_x = math.ceil(Def_of_pixels / ori_shape[0] )
        amount_of_increase_pixels_y = math.ceil(Def_of_pixels / ori_shape[1] )
        amount_of_increase_pixels_x = (amount_of_increase_pixels_x + ori_shape[1]) / ori_shape[1]
        amount_of_increase_pixels_y = (amount_of_increase_pixels_y + ori_shape[0]) / ori_shape[0]
        resized_img = cv2.resize(img, (0,0), fx=amount_of_increase_pixels_x, fy=amount_of_increase_pixels_y)
        ori_shape = resized_img.shape
        print(ori_shape)
        img = resized_img
    data = np.reshape(img, -1)
    for (idx, val) in enumerate(msg):
        encode(data[idx*BYTES_PER_BYTE: (idx+1) * BYTES_PER_BYTE], val)

    img = np.reshape(data, ori_shape)
    filename, _ = path.splitext(img_path)
    filename += '_lsb_embeded' + ".png"
    cv2.imwrite(filename, img)
    return filename

def encode(block, data):
    # returns the Unicode code from a given character
    data = ord(data)
    for idx in range(len(block)):
        block[idx] &= HIGH_BITS
        block[idx] |= (data >> (BITS * idx)) & LOW_BITS

if __name__ == '__main__':

    if len(sys.argv) == 3:
        img_path = sys.argv[1]
        msg = sys.argv[2]
    else:
        img_path = "./assets/ubuntu.jpg"
        msg = 'We got our man. Leave from the shipping port, gate B by Friday evening.'
    
    res_path = insert(img_path, msg)
    print("Successfully embedded.")
