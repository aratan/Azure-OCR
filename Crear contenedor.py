import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

account_url = "https://forms1data.blob.core.windows.net"
default_credential = DefaultAzureCredential()


# Crea el  BlobServiceClient object
blob_service_client = BlobServiceClient(account_url, credential=default_credential)

# Crea un nombre unico para el contenedor
container_name = str(uuid.uuid4())

# Crea el conitenedor con el nombre unico
container_client = blob_service_client.create_container(container_name)

# control de excepciones
try:
    print("Azure Blob Storage esta correcto")

    # Quickstart code goes here

except Exception as ex:
    print('Exception:')
    print(ex)


