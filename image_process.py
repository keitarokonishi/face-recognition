import cv2
import numpy as np
from keras.models import load_model

from measure import velocity_measurement
from config import cascade_path
from config import model_path

cascade = cv2.CascadeClassifier(cascade_path)
model = load_model(model_path)

# @velocity_measurement
def culc_kanna_value(face_list: list, image):
    for (x, y, w, h) in face_list:
        image = image[y:y+h, x:x+w]

        b, g, r = cv2.split(image)
        image = cv2.merge([r, g, b])
        img = cv2.resize(image, (64, 64))
        img = np.expand_dims(img, axis=0)

        kanna_probability_value = model.predict(img)[0][1]
        kanna_value = round(kanna_probability_value * 100, 1)

    return image, kanna_value

# @velocity_measurement
def get_face_list(image):
    # 顔認識の実行
    return cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(100, 100))

# @velocity_measurement
def pred_kanna(image):
    face_list = get_face_list(image)
    original_image = image

    if len(face_list) == 1:
        image, kanna_value = culc_kanna_value(face_list, image)
    else:
        kanna_value = 0

    return image, kanna_value, original_image
