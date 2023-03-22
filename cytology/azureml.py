from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Data,
    Environment,
    CodeConfiguration,
    ProbeSettings,
)
from azure.identity import DefaultAzureCredential
import os

from azure.ai.ml.constants import AssetTypes, InputOutputModes
from azure.ai.ml import Input

# enter details of your Azure Machine Learning workspace
subscription_id = "8850fa2d-2fec-446e-81ce-0866bd59fc04"
resource_group = "SeattleSlew"
workspace = "balmodels"

# get a handle to the workspace
ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# create endpoint
online_endpoint_name = "balmodels-test3"

endpoint = ManagedOnlineEndpoint(
    name=online_endpoint_name,
    description="this is a sample online endpoint for deploying model",
    auth_mode="key",
    tags={"foo": "bar"},
)

#ml_client.begin_create_or_update(endpoint).result()

deployment_name = "yolov5-1"

ml_client.online_endpoints.get(name=online_endpoint_name)

# register model

model_name = "yolov5"
model = Model(
    path="cytology/yolov5s-cls.pt",
    name=model_name,
    description="my sample object detection model",
    type=AssetTypes.CUSTOM_MODEL,
)

registered_model = ml_client.models.create_or_update(model)

env = Environment(
    image="mcr.microsoft.com/azureml/curated/acpt-pytorch-1.11-py38-cuda11.3-gpu:11",
)

deployment = ManagedOnlineDeployment(
    name="yolo-deploy",
    endpoint_name=online_endpoint_name,
    model=registered_model.id,
    instance_type="Standard_DS1_v2",
    environment=env,
    instance_count=1,
    liveness_probe=ProbeSettings(
        failure_threshold=30,
        success_threshold=1,
        timeout=2,
        period=10,
        initial_delay=2000,
    ),
    readiness_probe=ProbeSettings(
        failure_threshold=10,
        success_threshold=1,
        timeout=10,
        period=10,
        initial_delay=2000,
    ),
)

# Get the details for online endpoint
endpoint = ml_client.online_endpoints.get(name=online_endpoint_name)

# existing traffic details
print(endpoint.traffic)

# Get the scoring URI
print(endpoint.scoring_uri)

endpoint.traffic = {"yolo-deploy": 100}
ml_client.begin_create_or_update(deployment).result()

# Create request json
import base64

sample_image = "https://seattleslew.blob.core.windows.net/static/images/horse.jpeg"


def read_image(image_path):
    with open(image_path, "rb") as f:
        return f.read()


request_json = {
    "input_data": {
        "columns": ["image"],
        "data": [base64.encodebytes(read_image(sample_image)).decode("utf-8")],
    }
}

import json

request_file_name = "sample_request_data.json"

with open(request_file_name, "w") as request_file:
    json.dump(request_json, request_file)

resp = ml_client.online_endpoints.invoke(
    endpoint_name=online_endpoint_name,
    deployment_name=deployment.name,
    request_file=request_file_name,
)