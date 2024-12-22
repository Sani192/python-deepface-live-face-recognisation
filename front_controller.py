#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 21:34:25 2024

@author: anonymous
"""

from flask import Flask, send_from_directory, jsonify, request, copy_current_request_context
import concurrent.futures
from functools import wraps
import realtime_face_recognition
import dms

app = Flask(__name__)
executor = concurrent.futures.ThreadPoolExecutor(max_workers=15)

def run_in_thread(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        # Copy current request context
        @copy_current_request_context
        def run_and_capture():
            try:
                return f(*args, **kwargs)
            except Exception as e:
                print(f"Error occurred in thread: {e}")
                return None
        executor.submit(run_and_capture)
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

@app.route("/move-images")
@run_in_thread
def move_images():
    #data = request.get_json()
    #image_names = data.get('image_names')
    #new_directory = data.get('new_dir')
    print("inside moving images")
    #print(request)
    image_names = request.args.getlist('image_names')
    print(image_names)
    new_directory = request.args.get('new_dir')
    print(new_directory)
    dms.move_images(image_names, new_directory)
    return "", 202

@app.route("/list-directories")
def list_directories():
    print("going to list directories")
    directories = dms.list_directories()
    print(directories)
    #return jsonify({"directories": directories}), 202
    return directories, 202


@app.route("/load-image/<directory>/<filename>")     
def load_image(directory: str, filename: str):
    print("going to load image")
    dir_path = dms.load_image(directory, filename)
    print(dir_path)
    
    if dir_path:
        return send_from_directory(directory = str(dir_path), path = filename)
    
    return jsonify({"error": "Image not found"}), 404