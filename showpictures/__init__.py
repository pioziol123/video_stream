import azure.functions as func
from azure.storage.blob import BlobServiceClient
import json

url = "https://vreader.blob.core.windows.net/video-storage/"

def main(req: func.HttpRequest) -> func.HttpResponse:
    blob_service_client = BlobServiceClient.from_connection_string("storage key")
    container_name = "video-storage"

    images = [blob.name for blob in blob_service_client.get_container_client(container_name).list_blobs()]
    result = {
        "url": url,
        "images": images
    }
    return func.HttpResponse(json.dumps(result), headers={"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})
