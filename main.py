from joblib import load
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import numpy as np
import os
import urllib.request

print("Remove file")


print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")

print("This file directory only")
print(os.path.dirname(full_path))

for entry in os.scandir('.'):
    if entry.is_file():
        print(entry.name)
        
print("Get file")
urllib.request.urlretrieve("https://media.githubusercontent.com/media/wall-of-pain/iStroke/main/xgc_jlib", "xgc_jlib")

for entry in os.scandir('.'):
    if entry.is_file():
        print(entry.name)



# App Initialized
app = Flask(__name__)
api = Api(app)


def encode_hypertension(hypertension):
    if hypertension == 'yes':
        hypertension = 1
    else:
        hypertension = 0
    return hypertension


def encode_heart_disease(heart_disease):
    if heart_disease == 'yes':
        heart_disease = 1
    else:
        heart_disease = 0
    return heart_disease


def encode_married(married):
    if married == 'yes':
        married = 1
    else:
        married = 0
    return married


def encode_intensity(final_score):
    if final_score >= 40:
        intensity = 3
    elif final_score < 40 and final_score >= 15:
        intensity = 2
    elif final_score >= 0 and final_score < 15:
        intensity = 1
    return intensity


@app.route('/api/v1/', methods=['GET', 'POST'])
def data_fetch():

    # Get Data
    age = float(request.args.get('age'))
    avg_glucose_level = float(request.args.get('avg_glucose_level'))
    get_hypertension = str(request.args.get('hypertension')).lower()
    get_heart_disease = str(request.args.get('heart_disease')).lower()
    get_married = str(request.args.get('married')).lower()

    # Encode string values to int
    hypertension = encode_hypertension(get_hypertension)
    heart_disease = encode_heart_disease(get_heart_disease)
    married = encode_married(get_married)

    # Runner - Engine
    model = load('xgc_jlib')

    data_np_array = np.array(
        [[age, hypertension, heart_disease, married, avg_glucose_level]])

    len(data_np_array)

    data_final = model.predict_proba(data_np_array)[0][1]
    final_score = round(data_final*100, 6)
    intensity = encode_intensity(final_score)

    # Json data
    computed_json = {
        "Probability": str(final_score),
        "Intensity": int(intensity), }

    # Return Json
    return jsonify(computed_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
