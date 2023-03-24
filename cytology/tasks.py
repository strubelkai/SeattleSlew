#from celery import shared_task
import cv2
import torch
from django.conf import settings
from PIL import Image
import requests
from io import BytesIO
import os
from cytology.models import Sample
from django.core.files.storage import default_storage as storage

def rename_sample(widget_id, name):
    s = Sample.objects.get(id=widget_id)
    s.name = name
    s.save()

def YoloV5(f):
        print("Task for FILE NAME:", f)
        # Model
        model_url = os.path.join(settings.BASE_DIR, 'cytology/yolo/best.pt') 
        model = torch.hub.load('ultralytics/yolov5',  'custom', path=model_url, force_reload=True)
        
        # Images
        response =  storage.open(f).read()
        im1 = Image.open(BytesIO(response))
        
        # Inference
        results = model([im1], size=640) # batch of images

        # Results

        #results.print()  
        results.save(save_dir='staticfiles/images/', exist_ok=True)  # or .show()
        results.show()

        #results.xyxy[0]  # im1 predictions (tensor)
        #results.pandas().xyxy[0]  # im1 predictions (pandas)