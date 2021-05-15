""" exce function """
# coding: utf-8

""" public module """
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

""" private module """
from image_process import pred_kanna
from image import read_image, save_image
# from logger import create_logfile
from config import save_dir
from config import log_dir
from config import measured_dir
from config import model_dir
from config import port_number
from config import host_ip_address

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

if not os.path.isdir(measured_dir):
    os.mkdir(measured_dir)

if not os.path.isdir(model_dir):
    os.mkdir(model_dir)

app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    return render_template('index.html', images=os.listdir(save_dir)[::-1])

@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory(save_dir, path)

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
    port = int(os.environ.get("PORT", port_number))
    # create_logfile()
    app.run(host=host_ip_address, port=port)
