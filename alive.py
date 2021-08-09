from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "난 살아있음"
def run():
  app.run('0.0.0.0',8080)
def alive():
  t = Thread(target=run)
  t.start()