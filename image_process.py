import cv2
import numpy as np
from keras.models import load_model

cascadePath = './haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascadePath)
model = load_model('./my_model.h5')

def pred_kanna(image):

#   cascadePath = './haarcascade_frontalface_alt.xml'
#   cascade = cv2.CascadeClassifier(cascadePath)
#   model = load_model('./my_model.h5')

  # 顔認識の実行
  face_list = cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=1, minSize=(100,100))
  
  original_image = image

  if len(face_list) == 1:
    for rect in face_list:
      image = image[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
      b,g,r = cv2.split(image)
      image = cv2.merge([r,g,b])
      img = cv2.resize(image,(64, 64))
      img = np.expand_dims(img, axis=0)
      
      kanna_value = model.predict(img)[0][1]
      kanna_value = round(kanna_value * 100, 1)
  else:
    image = original_image
    kanna_value = 0

  return image, kanna_value, original_image
