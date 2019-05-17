from flask import Flask
from flask import request, jsonify, abort
from git import Repo
import os
import hmac

app = Flask(__name__)

GITHUB_SECRET_TOKEN = os.environ.get('GITHUB_SECRET')
REPO_PATH = os.environ.get('REPO_PATH')
HTML_PATH = os.environ.get('HTML_PATH')


def gitpulldeployed():
    repo = Repo(REPO_PATH)
    origin = repo.remotes.origin
    #origin.pull('--rebase')
    origin.pull()
    a = os.system('cd '+REPO_PATH+"; git submodule update")
    return a

def hugodeployed():
    a = os.system("cd {0}; hugo --baseUrl=''".format(REPO_PATH))
    return a

def htmldeployed():
    a = os.system("\cp -rf {0}public/* {1}".format(REPO_PATH,HTML_PATH))
    return a

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        signature = request.headers.get('X-Hub-Signature')
        sha, signature = signature.split('=')
        secret = str.encode(GITHUB_SECRET_TOKEN)
        hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
        if hmac.compare_digest(hashhex, signature):
            a = gitpulldeployed()
            b = hugodeployed()
            c = htmldeployed()
            return jsonify({'status': 'success','gitpull': a,'hugo': b,'html': c}), 200
        else:
            return jsonify({'status': 'bad token'}), 401
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8088')