import pymongo #pip install pymongo
from flask import Flask, render_template # pip install flask
from ssh_pymongo import MongoSession # pip install ssh-pymongo


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/adminView')
def adminView():
    return render_template('adminView.html')
    
@app.route('/analystView')
def analystView():
    return render_template('analystView.html')

@app.route('/userView')
def userView():
    return render_template('userView.html')


@app.route('/req1')
def req1():
    return render_template('req.html')


@app.route('/req2')
def req2():
    return render_template('req.html')


@app.route('/req3')
def req3():
    return render_template('req.html')


@app.route('/req4')
def req4():
    return render_template('req.html')


@app.route('/req5')
def req5():
    return render_template('req.html')


@app.route('/req6')
def req6():
    return render_template('req.html')


@app.route('/req7')
def req7():
    return render_template('req.html')


@app.route('/req8')
def req8():
    return render_template('req.html')

if __name__ == "__main__":
    app.run()