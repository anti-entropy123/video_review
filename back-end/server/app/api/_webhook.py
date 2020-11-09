from flask import request
from . import api
import os
import threading

@api.route('/_webhook', methods=['GET', 'POST'])
def test_webhook():
    data = request.json
    # print(data)
    branch = data['ref'].split('/')[-1]
    print(branch)
    if branch == 'master':
        threading.Thread(
            target=lambda: print(os.system("bash /home/ubuntu/yjn/video_review/back-end/server/update.sh"))
        ).start()
    
    return "OK"