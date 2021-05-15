""" exce function """
# coding: utf-8

""" public module """
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
import os
import string
import random
from datetime import datetime

""" private module """
from measure import velocity_measurement
from image_process import pred_kanna
from config import save_dir
from config import log_dir
from config import measured_dir
from config import model_dir

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

if not os.path.isdir(measured_dir):
    os.mkdir(measured_dir)

if not os.path.isdir(model_dir):
    os.mkdir(model_dir)

app = Flask(__name__, static_url_path="")

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(save_dir)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(save_dir, path)

@velocity_measurement
def read_image(image):
    stream = image.stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)
    return img

@velocity_measurement
def save_image(kanna_value, original_image):
    # リサイズ
    width = 200
    height = width * (original_image.shape[0] / original_image.shape[1])
    original_image = cv2.resize(original_image , (int(width), int(height)))
    
    dt_now = str(kanna_value) + "_original_" + datetime.now().strftime("%Y_%m_%d%_H_%M_%S_") + random_str(5)
    save_filename = dt_now + ".png"
    save_path = os.path.join(save_dir, save_filename)
    cv2.imwrite(save_path, original_image)

    return save_filename, save_path

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        img = read_image(request.files['image'])

        # 変換
        img, kanna_value, original_image = pred_kanna(img)

        # オリジナル画像を保存
        save_filename, save_path = save_image(kanna_value, original_image)

        return render_template('result.html', filename=save_filename, kanna_value=kanna_value)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))

    logger.create_logfile()

    app.run(host='0.0.0.0', port=port)
