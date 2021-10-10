from flask import Flask
import os

env_var = os.getenv('MESSAGE')

app = Flask(__name__)

@app.route('/')
def home():
    return 'The message is : ' + env_var + ". Bye!"
