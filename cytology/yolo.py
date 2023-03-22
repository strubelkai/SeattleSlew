import cv2
import torch
from django.conf import settings
from PIL import Image
import requests
from io import BytesIO
import os

STATIC_LOCATION = "static"
MEDIA_LOCATION = "media"


AZURE_ACCOUNT_NAME = "seattleslew"
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
AZURE_CONTAINER = "static"
AZURE_ACCOUNT_KEY = os.environ['AZURE_STORAGE_KEY']
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

def YoloV5(f):

        print("FILE NAME:", f)
        # Model
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        
        # Images
        response = requests.get('https://seattleslew.blob.core.windows.net/static/' + f)
        im1 = Image.open(BytesIO(response.content))

        # Inference
        results = model([im1], size=640) # batch of images

        # Results

        #results.print()  
        results.save(save_dir='staticfiles/images/', exist_ok=True)  # or .show()
        results.show()

        #results.xyxy[0]  # im1 predictions (tensor)
        #results.pandas().xyxy[0]  # im1 predictions (pandas)