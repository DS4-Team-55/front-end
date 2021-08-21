from flask import Flask, request, Response
from werkzeug.utils import secure_filename
import numpy as np
import os
import json
import pickle

app = Flask(__name__)

morb_model_path = 'models/morbidity-model.pkl'
'''
with open(morb_model_path, 'rb') as file:
    morbidity_model = pickle.load(file)
'''
lw_model_path = 'models/low-weight-model.pkl'
with open(lw_model_path, 'rb') as file:
    low_weight_model = pickle.load(file)


@app.route('/morbidity', methods = ['GET', 'POST'])
def morbidity_prediction():
    data = json.loads(request.data)
    resp = json.dumps({'prediction': round(np.random.rand() * 100, 2)})
    return Response(resp, mimetype='application/json')

@app.route('/low_weight', methods = ['GET', 'POST'])
def low_weight_prediction():
    data = json.loads(request.data)
    pred = low_weight_model.predict_proba(np.array(list(data.values())).reshape(1, -1))[0][1]
    resp = json.dumps({'prediction': round(pred * 100, 2)})
    return Response(resp, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug = True)