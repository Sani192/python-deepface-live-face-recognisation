This project is used for face recognition when you already set up faces in the faces folder. It will recognize the face and speak the name.
I have created this project using Python with deepface learning. I used the OpenCV library and Python text-to-speech3 (pyttsx3).

It will continuously speak the recognized person's name every 3 seconds. If you want to stop the running app then press the 'q' and it will stop the app.

I have added Flask so that I can call the endpoint (HTTP request) to my Python script. Below are the steps I follow to run the script:
1) flask --app front_controller run --host=<local_ip_address> --port=5000
2) http://<local_ip_address>:5000/live-face-recognition/start
