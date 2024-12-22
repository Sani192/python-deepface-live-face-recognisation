#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 22:01:10 2024

@author: anonymous
"""

import os
import shutil
from pathlib import Path

FACES_DIR = Path("faces")

def move_images(image_names, new_directory):
    print(image_names)
    #print(new_directory)
    target_directory = os.path.join("faces", new_directory)
    print(target_directory)
    
    # Create new directory if doesn't exists
    os.makedirs(target_directory, exist_ok=True)
    
    counter = 1
    
    # Move images
    for image_name in image_names:
        source_path = os.path.join('faces/Unknown', image_name)
        file_extension = os.path.splitext(image_name)[1]
        
        # Generate new unique filename
        while True:
            new_image_name = f"{new_directory}_{counter}{file_extension}"
            destination_path = os.path.join(target_directory, new_image_name)
            print(destination_path)
            if not os.path.exists(destination_path):
                break
            counter += 1
        
        if os.path.exists(source_path):
            print("moving....")
            shutil.move(source_path, destination_path)
            counter += 1
        else:
            print(f'Image {image_name} not found in Unknown directory')
        
    return True

def list_directories():
    directories = {}
    
    for directory in FACES_DIR.iterdir():
        if directory.is_dir():
            images = [image.name for image in directory.glob("*.jpg") if image.is_file()]
            directories[directory.name] = images
            
    return directories
    
def load_image(directory: str, filename: str):
    dir_path = FACES_DIR / directory
    
    if dir_path.exists() and (dir_path / filename).exists():
        return str(dir_path)
    
    return ""
    
    
    
    
    
    