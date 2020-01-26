
from base64 import b64decode
import azure.functions as func
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {"Access-Control-Allow-Origin": "*"}
    try:
        blob_service_client = BlobServiceClient.from_connection_string("storage key")
        container_name = "video-storage"
        picture_name = req.params.get('name')
        req_body = req.get_json()
        data = b64decode(req_body.get('picture'))
        
        blob_client = blob_service_client.get_blob_client(container_name, blob=picture_name)
        blob_client.upload_blob(data)
        return func.HttpResponse("OK",
            headers=headers, status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e),
            headers=headers, status_code=200)