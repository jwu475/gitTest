## Intergrate HTML with Flask
## HTML verb GET, POST

## Jinja2 template engine
'''
{%...%} for statements
{{ }} expression to print output
{#...#} this is for comments
'''

from flask import Flask, redirect, url_for, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
#from sklearn.preprocessing import StandardScaler

### WSGI Application
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

#declarator
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/submit", methods=['POST'])
def predict():

    Generated_Power = 0
    queryValue = []
    if request.method == 'POST':
        Time = request.form['time']

        queryValue.append(float(request.form['GT_exhaustTemp']))

        queryValue.append(float(request.form['Comp_inletTemp']))

        queryValue.append(float(request.form['IGV_angleInlet']))

        queryValue.append(float(request.form['Compressor_disPress']))

        queryValue.append(float(request.form['Compressor_disTemp']))

        query_data = scaler.transform(np.asarray(queryValue).reshape(1, 5))
        #query_data = np.asarray(queryValue).reshape(1, 5)
        
        prediction = model.predict(query_data)[0]
        
        return render_template('index.html',predicted_power="The predicted power generation is {0:.4f} MW.".format(prediction))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=False, host='0.0.0.0', port=80)
    #app.run(host='0.0.0.0', port= 8080) #debug=True)  # ru on  http://localhost:8080/