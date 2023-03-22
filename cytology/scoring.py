import json
import numpy as np
import onnxruntime
import sys
import os
from azureml.core.model import Model
import time
from json_tricks import dumps

def init():
    global session, input_name, output_name
    model = Model.get_model_path(model_name = 'yolov5')
    session = onnxruntime.InferenceSession(model, None)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name 
    
def run(input_data):
    '''Purpose: evaluate test input in Azure Cloud using onnxruntime.
        We will call the run function later from our Jupyter Notebook 
        so our azure service can evaluate our model input in the cloud. '''
    try:
        # load in our data, convert to readable format
        data = np.array(json.loads(input_data)['data']).astype('float32')
        start = time.time()
        r = session.run([output_name], {input_name: data})[0]
        end = time.time()
        serialised = dumps(r)
        result_dict = {"result": serialised,
                      "time_in_sec": [end - start]}
    except Exception as e:
        result_dict = json.dumps({"error": str(e)})
    return result_dict