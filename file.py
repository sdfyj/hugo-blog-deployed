#coding:utf-8
from flask import request, Flask,jsonify,abort
import time
import os
app = Flask(__name__)


REPO_PATH = os.environ.get('REPO_PATH')
HTML_PATH = os.environ.get('HTML_PATH')
FILE_PATH = os.path.join(REPO_PATH,'..','file/')
IMG_PATH = os.path.join(HTML_PATH,'imgfile/')

def htmldeployed():
    a = os.system("\cp -rf {0}* {1}".format(FILE_PATH,IMG_PATH))
    return a

@app.route("/", methods=['POST'])
def get_frame():
    start_time = time.time()
    upload_file = request.files['file']
    old_file_name = upload_file.filename
    if upload_file:
        file_path = os.path.join(FILE_PATH, old_file_name)
        upload_file.save(file_path)
        htmldeployed()
        duration = time.time() - start_time
        ts = '[%.0fms]' % (duration*1000)
        print('success',ts)
        return  jsonify({'status': 'success','duration':ts}),200
    else:
        return jsonify({'status': 'failed'}), 401


if __name__ == "__main__":
    app.run("0.0.0.0", port=8001)