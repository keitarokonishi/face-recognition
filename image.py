"""image transform method."""
import os
import string
import random
from datetime import datetime

import numpy as np
import cv2

from measure import velocity_measurement
from config import save_dir

@velocity_measurement
def read_image(image):
    stream = image.stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)
    return img

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@velocity_measurement
def save_image(kanna_value, original_image):
    # リサイズ
    width = 200
    height = width * (original_image.shape[0] / original_image.shape[1])
    original_image = cv2.resize(original_image , (int(width), int(height)))
    
    dt_now = str(kanna_value) + "_original_" + datetime.now().strftime("%Y_%m_%d%_H_%M_%S_") + random_str(5)
    save_filename = f"{dt_now}.png"
    save_path = os.path.join(save_dir, save_filename)
    cv2.imwrite(save_path, original_image)

    return save_filename, save_path
