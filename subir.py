
import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Define the connection string and container name where you want to upload the file
connect_str = "DefaultEndpointsProtocol=https;AccountName=forms1data;AccountKey=oG0Df044zf6F9DmVFc+WCvXuDTKyzuQ1Eg2MXXRE7htF/znqpy4LeUcqE0RBiE0AMxPx5Jiwh0do+AStvoygBg==;EndpointSuffix=DefaultEndpointsProtocol=https;AccountName=forms1data;AccountKey=BOiI3LOElagQIo0mQFdsrc2osUI449luokTjrW39rkDMf78bhpbu9mLsdH4m2R5HLDQzx55LsciY+AStThoSaQ==;EndpointSuffix=core.windows.net"
container_name = "e8bbaf0b-d164-4417-92c4-f9aaba63cc88"

# Define the name of the file to upload
file_name = "subir.py"

# Create a BlobServiceClient object from the connection string
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

# Create a BlobClient object for the file you want to upload
blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

# Upload the file to Azure Blob Storage
with open(file_name, "rb") as data:
    blob_client.upload_blob(data)

print("File has been uploaded to Azure Blob Storage.")