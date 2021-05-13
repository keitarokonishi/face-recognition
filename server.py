from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import numpy as np
import cv2
from image_process import pred_kanna
from datetime import datetime
import os
import string
import random

from logging.config import dictConfig
import datetime

SAVE_DIR = "./images"
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)

app = Flask(__name__, static_url_path="")

def random_str(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(SAVE_DIR)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(SAVE_DIR, path)

# 参考: https://qiita.com/yuuuu3/items/6e4206fdc8c83747544b
@app.route('/upload', methods=['POST'])
def upload():
    if request.files['image']:
        # 画像として読み込み
        stream = request.files['image'].stream
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)

        # 変換
        img, kanna_value, original_image = pred_kanna(img)

        # オリジナル画像を保存
        # リサイズ
        width = 200
        height = width * (original_image.shape[0] / original_image.shape[1])
        original_image = cv2.resize(original_image , (int(width), int(height)))
        
        dt_now = str(kanna_value) + "_original_" + datetime.now().strftime("%Y_%m_%d%_H_%M_%S_") + random_str(5)
        save_filename = dt_now + ".png"
        save_path = os.path.join(SAVE_DIR, save_filename)
        cv2.imwrite(save_path, original_image)

        return render_template('result.html', filename=save_filename, kanna_value=kanna_value)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))

    dt_now = datetime.datetime.now()
    current_date = dt_now.strftime("%Y-%m-%d")
    logger_file_dir = '/storage/logs/face-recognition_{}.log'.format(current_date)

    dictConfig({
        'version': 1,
        'formatters': {
            'file': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'file',
            'filename': '{}'.format(logger_file_dir),
            'backupCount': 3,
            'when': 'D',
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['file']
        }
    })

    app.run(host='0.0.0.0', port=port)
