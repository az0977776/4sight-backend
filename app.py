#!/usr/bin/env python
from flask import Flask, render_template, Response, request
from video import Video
from sql import SQLConnection
from datetime import datetime, timedelta

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

def gen(video):
    while True:
        frame = video.get_frame()
        if not frame:
            frame = b""
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream/<f_id>', methods=['GET'])
def stream(f_id):
    return Response(gen(Video(f_id)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/feed/<f_id>', methods=['GET'])
def feed(f_id):
    db = SQLConnection()
    return db.get_feed(f_id)

@app.route('/areas', methods=['GET'])
def areas():
    # https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    # using different connection and cursor instead of not checking same thread, in case of data corruption
    db = SQLConnection()
    return db.get_all_area()

@app.route('/area_feeds/<a_id>', methods=['GET'])
def feeds(a_id):
    db = SQLConnection()
    return db.get_area_feeds(a_id)

@app.route('/counts/<a_id>', methods=['GET'])
def count(a_id):
    db = SQLConnection()
    return db.get_counts(a_id, time_start=datetime.now() - timedelta(days=1))

@app.route('/predictions/<a_id>', methods=['GET'])
def prediction(a_id):
    db = SQLConnection()
    return db.get_predictions(a_id, time_end=datetime.now() + timedelta(days=1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
