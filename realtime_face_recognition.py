#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:35:47 2024

@author: anonymous
"""


from deepface import DeepFace
from speaker import Speaker
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
similarity_threshold = 0.4

# Path to the image for face recognition
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
            # Perform face recognition on the captured frame
            # Find faces and identify people using a specific model and distance metric
            people = DeepFace.find(img_path=frame, db_path="faces/", model_name=models[0], distance_metric=metrics[2])
            #print(people)
            
            # Filter the results based on similarity threashold
            #filtered_results = [p for p in people if p['distance'][0] <= similarity_threshold]
            #print("==========================================================++++++")
            #print(filtered_results)
    
            #print("================================================================")
            #print(len(people))
            #print("==========================================================------")
            #print(people)
            for person in people:
                #print(len(person))
                if not len(person):
                    continue
                
                #print(person)
                #print("Distance is: " + person['distance'])
                if person['distance'][0] > similarity_threshold:
                    speaker.announce('Unknown')
                    img_name = "Unknown_{}.jpg".format(int(time.time()))
                    cv2.imwrite(os.path.join(unknown_faces_dir, img_name), frame)
                    print("{} written!".format(img_name))
                    continue
                
                # Retrieve the coordinates of the face bounding box
                # x = person['source_x'][0]
                # y = person['source_y'][0]
                # w = person['source_w'][0]
                # h = person['source_h'][0]
    
                # Draw a rectangle around the face
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
                # Get the person's name and display it on the image
                name = person['identity'][0].split('/')[1]
                print("Response: " + name)
                speaker.announce(name)
                #time.sleep(3)
                #cv2.putText(frame, name, (x, y), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)
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