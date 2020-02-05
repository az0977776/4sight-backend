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

@app.route('/feed', methods=['GET'])
def feed():
    return Response(gen(Video(request.args.get('f_id'))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/areas', methods=['GET'])
def areas():
    # https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    # using different connection and cursor instead of not checking same thread, in case of data corruption
    db = SQLConnection()
    return db.get_all_area()

@app.route('/feeds/<a_id>', methods=['GET'])
def feeds(a_id):
    db = SQLConnection()
    return db.get_area_feeds(a_id)

@app.route('/counts/<f_id>', methods=['GET'])
def count(f_id):
    db = SQLConnection()
    return db.get_counts(f_id, time_start=datetime.now() - timedelta(days=1))

@app.route('/predictions/<f_id>', methods=['GET'])
def prediction(f_id):
    db = SQLConnection()
    return db.get_predictions(f_id, time_end=datetime.now() + timedelta(days=1))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
