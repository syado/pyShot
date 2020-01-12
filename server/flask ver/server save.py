import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from urllib.parse import urlparse
import hashlib
import time
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():    
    id = request.form["id"]
    imagedata = request.files["imagedata"].stream.read()
    
    hash = hashlib.md5(imagedata).hexdigest()
    if not id or id == "":
        id = hashlib.md5(request.remote_addr+str(time.time())).hexdigest()
        
    filename = secure_filename(hash+".png")
    img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    u = urlparse(request.base_url)
    with open(img_url, mode='wb') as f:
        f.write(imagedata)
    return u.scheme +"://" + u.netloc + "/" + img_url
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=80)