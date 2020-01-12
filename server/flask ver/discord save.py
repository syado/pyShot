# coding: UTF-8

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from urllib.parse import urlparse
import hashlib
import time
import io
from discord import Webhook, RequestsWebhookAdapter, File

webhook_url = "https://discordapp.com/api/webhooks/xxxx/xxxxxxxxxxxxxxxx"
avatar_url = "https://xxxx.com/xxxxx.png"
username = "Gyazo by syado"
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():    
    imagedata = request.files["imagedata"].stream.read()
    hash = hashlib.md5(imagedata).hexdigest()
        
    filename = secure_filename(hash+".png")
    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    u = urlparse(request.base_url)
        
    res = None
    for i in range(5):
        try:
            res = webhook.send(username=username, avatar_url=avatar_url, file=File(fp=io.BytesIO(imagedata),filename=filename))
            return res["attachments"][0]["url"]
        except:
            time.sleep(1)
            pass
    with open(img_url, mode='wb') as f:
        f.write(imagedata)
    return u.scheme +"://" + u.netloc + "/" + img_url
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)