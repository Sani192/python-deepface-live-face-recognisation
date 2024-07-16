#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:08:23 2024

@author: anonymous
"""

import pyttsx3
import threading

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        
    def speak(self, text):
        if self.engine._inLoop:
            self.engine.endLoop()
        threading.Thread(target=self._speak_thread, args=(text,)).start()
        
    def _speak_thread(self, text):
        self.engine.say(text)
        self.engine.runAndWait()