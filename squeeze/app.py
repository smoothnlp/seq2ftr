from transformer import SequenceTransformer

import json
from flask import Flask, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

st = SequenceTransformer()

@app.route('/squeeze', methods=['POST'])
def feature():
    data = request.get_json()
    res = st.transform(data)
    return Response(
        response=json.dumps(res),
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9600, debug=True)
