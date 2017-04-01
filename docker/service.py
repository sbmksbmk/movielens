from flask import Response
from flask import Flask
from flask import request
from flask import session
import json

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
login_keys = ['userid', 'name', 'email']

def check_login():
    if 'userid' in session:
        return True
    else:
        return False

def login_success(keys):
    for key in login_keys:
        try:
            session[key] = keys.get(key, None)
        except:
            pass

def logout_event():
    for key in login_keys:
        session.pop(key, None)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    msg = {'msg': 'test index message'}
    return Response(json.dumps(msg), status=200)

@app.route('/test/', methods=['POST', 'GET'])
def test():
    if check_login() is True:
        print session
        msg = {'msg': 'your id is {}'.format(session['userid'])}
        return Response(json.dumps(msg), status=200)
    else:
        msg = {'msg': 'wrong message'}
        return Response(json.dumps(msg), status=401)

@app.route('/testpost/', methods=['POST', 'GET'])
def pdata():
    print request.json
    msg = {'msg': 'test post message'}
    return Response(json.dumps(msg), status=200)

@app.route('/login', methods=['POST', 'GET'])
def login():

    print request.args
    print request.json
    if request.args['userid'] is not None:
        print request.args['userid']
        login_success(request.args)
        msg = {'msg': 'success message'}
        return Response(json.dumps(msg), status=200)
    else:
        msg = {'msg': 'wrong message'}
        return Response(json.dumps(msg), status=401)

if __name__ == '__main__':
    app.run(debug=True)
