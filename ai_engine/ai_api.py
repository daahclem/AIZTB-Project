# Flask API to expose AI scoring endpoint
from flask import Flask, request, jsonify
from risk_model import load_model, evaluate_risk
import torch
import numpy as np
from utils import extract_features

app = Flask(__name__)
model = load_model()

@app.route('/risk_score', methods=['POST'])
def risk_score():
    data = request.json
    features = extract_features(data)
    score = evaluate_risk(model, features)
    return jsonify({'risk_score': float(score)})

if __name__ == '__main__':
    app.run(port=5001)
