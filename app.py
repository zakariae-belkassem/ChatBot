from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from Chat_Inter_optimisé1 import startChat, getquestion

app = Flask(__name__)



@app.after_request
def add_header(response):
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def Predict():
    res = getquestion()
    response = jsonify({'result': res})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/chat', methods=['POST'])
def Chat():
    data = request.get_json()
    msg = data.get('text', '')
    res = startChat(msg)
    response = jsonify({'result': res, "user": msg})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run()
