import flask
from flask import Flask, render_template, request,jsonify
import recom
import numpy as np



app=Flask(__name__)
@app.route('/',methods=['GET'])
def Home():
 return render_template('index.html')

@app.route('/Team',methods=['GET'])
def Team():
 return render_template('Team.html')

@app.route('/predict', methods=['POST'])
def predict():
   # print("hello ")
    get_o = list()
    get=list()
    
    if request.method == 'POST':
       
        user = int(request.form['user'])
        #print("HIIII",user)
        
        get_o = [user]
        #print("GET_O=",get_o)
        k=10
        
        #data = np.array([get_o])
        #print("Data= ",data)
        get=recom.recommendation(get_o[0],k)
        #print("get=",get)
        return render_template("result.html", getit=get)
'''
@app.route('/rec',methods=['GET'])
def rec():
    active_user=1936617
    k=10
    
    get_n=list()
    get_n=recomm_try.recommendation(active_user,k)
    return render_template("index-1.html", getit=get_n)
'''

app.run(debug=True)
