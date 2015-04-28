import os
import uuid
import time
import json

from flask import Flask

app = Flask(__name__)
app.debug = True

def check(endpoint):
    def actual_check(function):
        start_time = time.time()
        ret = function()
        total_time = time.time() - start_time
        return json.dumps({
            'status': ret,
            'time': total_time
        })
    return app.route(endpoint)(actual_check)


@check('/nfs/home')
def nfs_home_check():
    content = str(uuid.uuid4())
    path = os.path.join('/data/project/canary/nfs-test/', content)
    try:
        with open(path, 'w') as f:
            f.write(content)

        with open(path) as f:
            actual_content = f.read()

        if actual_content == content:
            return True
        return False
    finally:
        os.remove(path)
