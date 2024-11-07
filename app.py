from flask import Flask
app = Flask(__name__)

@app.route('/')
def backend_ml():
    return 'Backend dla ML!'

@app.route('/rangers')
def hello_rangers():
    return 'Hello Rangers!'