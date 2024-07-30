#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 21:34:25 2024

@author: anonymous
"""

from flask import Flask, jsonify
import concurrent.futures
from functools import wraps
import realtime_face_recognition

app = Flask(__name__)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)

def run_in_thread(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        executor.submit(f, *args, **kwargs)
        return jsonify({"status": "success"}), 202
    return wrapped_function

@app.route("/")
def home():
    return "<p>Welcome to live face recognition</p>"

@app.route("/live-face-recognition/start")
@run_in_thread
def live_face_recognition_start():
    realtime_face_recognition.live_face_recognition_start()
    return "", 202
    
    
@app.route("/live-face-recognition/stop")
@run_in_thread
def live_face_recognition_stop():
    realtime_face_recognition.live_face_recognition_stop()
    return "", 202