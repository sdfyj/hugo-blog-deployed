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

def hugodeployed():
    os.system('cd '+REPO_PATH+'; hugo')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        signature = request.headers.get('X-Hub-Signature')
        sha, signature = signature.split('=')
        secret = str.encode(GITHUB_SECRET_TOKEN )
        hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
        if hmac.compare_digest(hashhex, signature):
            gitpulldeployed()
            hugodeployed()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8088')