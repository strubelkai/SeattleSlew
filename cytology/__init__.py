import os

from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
from azure.core.exceptions import ResourceExistsError

account_name = 'seattleslew' # Must be replaced by your <storage_account_name>
url = "https://{}.blob.core.windows.net".format(account_name)
shared_access_key = os.environ['AZURE_STORAGE_KEY']

blob_service_client = BlobServiceClient(account_url=url, credential=shared_access_key)

media_container_client = blob_service_client.get_container_client("media")
static_container_client = blob_service_client.get_container_client("static")

try:
    # [START create_container]
    media_container_client.create_container()
    static_container_client.create_container()

except ResourceExistsError:
            pass