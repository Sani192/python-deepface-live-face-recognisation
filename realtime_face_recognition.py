#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:35:47 2024

@author: anonymous
"""


from deepface import DeepFace
from speaker import Speaker
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import sys
import select
import threading
import os

# List of available backends, models, and distance metrics
backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
metrics = ["cosine", "euclidean", "euclidean_l2"]
similarity_threshold = 1.0

# Path to the image for face recognition
FACES_DIR = Path("faces")
EXCLUDE_DIR = "Unknown"
img = "faces/sani/sani_1.jpg"
unknown_faces_dir = "faces/Unknown"
os.makedirs(unknown_faces_dir, exist_ok=True)

# text to speech
speaker = Speaker()

# Shared variable and lock
stop_flag = False
stop_lock = threading.Lock()

# video url
video_url = "http://0.168.29.170/video"

def create_symlinks():
    image_paths = [
        str(img) for subdir in FACES_DIR.iterdir()
        if subdir.is_dir() and subdir.name != EXCLUDE_DIR
        for img in subdir.glob("*") if img.is_file()
        ]
    return image_paths    

def face_recognition(img):
    # Perform face recognition on the provided image
    # Find faces and identify people using a specific model and distance metric
    people = DeepFace.find(img_path=img, db_path="faces/", model_name=models[2], distance_metric=metrics[1])

    # Display the original image
    plt.imshow(cv2.imread(img))

    # Print the identities of the recognized people
    for person in people:
        print(person['identity'][0].split('/')[1])

def live_face_recognition_start():
    #dir_to_search = create_symlinks()
    
    # Define a video capture object
    vid = cv2.VideoCapture(0)
    
    global stop_flag
    while True:
        with stop_lock:
            if stop_flag:
                print("Live face recognition :: stopped")
                break
        
        # Capture the video frame by frame
        ret, frame = vid.read()
        
        if not ret:
            break
        
        try:
            # Extract faces
            extracted_faces = DeepFace.extract_faces(img_path = frame, detector_backend = backends[0], enforce_detection = False)
            print("===================Extracted faces")
            print(len(extracted_faces))
            print(extracted_faces)
            
            for face in extracted_faces:
                face_image = face["face"]
                print("===================face_image")
                print(face_image)
                
                # Find faces and identify people using a specific model and distance metric
                people = DeepFace.find(img_path=face_image, db_path="faces/", model_name=models[0], distance_metric=metrics[2], enforce_detection=False)
                print("===================people")
                print(len(people))
                print(people)
                
                # If no match found
                if len(people) == 0 or people[0]['distance'].min() > similarity_threshold or people[0]['identity'][0].split('/')[1] == EXCLUDE_DIR:
                    print("=====Distance")
                    #print(people[0]['distance'])
                    print(people[0]['distance'].min())
                    
                    # Convert face_img to 8-bit format
                    face_img_8bit = cv2.normalize(face_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
                    
                    # Convert face_img to BGR
                    face_bgr = cv2.cvtColor(face_img_8bit, cv2.COLOR_RGB2BGR)
                    
                    speaker.announce('Unknown')
                    img_name = "Unknown_{}.jpg".format(int(time.time()))
                    cv2.imwrite(os.path.join(unknown_faces_dir, img_name), face_bgr)
                    print("{} written!".format(img_name))
                    continue
                
                # Get the person's name and display it on the image
                print("=========Going to speak name")
                name = people[0]['identity'][0].split('/')[1]
                print("Response: " + name)
                speaker.announce(name)
                        
        except Exception as error:
            print("Exception occurred...")
            print(error)                

        # Display the resulting frame
        #cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('frame', 960, 720)
        #cv2.imshow('frame', frame)
        
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.read(1)
            print("Line " + line)
            if line == 'q':
                break
        
        time.sleep(3)

        # Check if the 'q' button is pressed to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("quiting.....")
            break

    # Release the video capture object and close all windows
    vid.release()
    cv2.destroyAllWindows()
    
    # Resetting flag so that again I can start
    # global stop_flag
    with stop_lock:
        stop_flag = False

def live_face_recognition_stop():
    global stop_flag
    with stop_lock:
        stop_flag = True
    print("Live face recognition stop flag set to True")

# Perform face recognition on a single image
#face_recognition(img)

# Perform real-time face recognition using the webcam
#live_face_recognition_start()