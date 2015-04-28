import os
import uuid
import time
import json

from flask import Flask

app = Flask(__name__)
app.debug = True


def check(endpoint):
    def actual_decorator(func):
        def actual_check():
            start_time = time.time()
            try:
                ret = func()
            except:
                # FIXME: log this error somewhere
                ret = False
            total_time = time.time() - start_time
            return json.dumps({
                'status': ret,
                'time': total_time
            })
        return app.route(endpoint)(actual_check)
    return actual_decorator


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
