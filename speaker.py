#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:31:04 2024

@author: anonymous
"""

from text_to_speech import TextToSpeech

class Speaker:
    def __init__(self):
        self.tts = TextToSpeech()
        
    def announce(self, message):
        self.tts.speak("Hello " + message)