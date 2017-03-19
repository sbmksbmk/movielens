from flask import Response
from flask import Flask
from flask import request
from flask import session
import json

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    msg = {'msg': 'test index message'}
    return Response(json.dumps(msg), status=200)


if __name__ == '__main__':
    app.run(debug=True)
