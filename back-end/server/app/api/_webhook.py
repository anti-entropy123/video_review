from flask import request
from . import api

@api.route('/_webhook', methods=['GET', 'POST'])
def test_webhook():
    data = request.json
    print(data)
    branch = 

    return "OK"