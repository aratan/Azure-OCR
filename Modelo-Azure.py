import json
from azure.ai.formrecognizer import DocumentModelAdministrationClient
from azure.core.credentials import AzureKeyCredential
import os
import pandas as pd
from dotenv import load_dotenv

# cargamos variable de entorno
load_dotenv()
endpoint = os.getenv('ENDPOINT')
key = os.getenv('API_KEY')

# Configuración de las credenciales de Azure
endpoint = "https://test-name-2023.cognitiveservices.azure.com/"
credential = AzureKeyCredential("dd95ab1fb8174c84940ec78126c8aa21")
document_model_admin_client = DocumentModelAdministrationClient(endpoint, credential)

# URL del contenedor de blobs de Azure donde se encuentran los archivos
container_sas_url = "https://partesamistosos.blob.core.windows.net/ocr?sp=racwdli&st=2023-03-17T09:49:00Z&se=2023-03-17T17:49:00Z&spr=https&sv=2021-12-02&sr=c&sig=fO21SV4Ai2dG3w1OHrfrKQSLkgOJZdYIsJVWGFeC5u0%3D"  # training documents uploaded to blob storage

# Lectura de los archivos CSV y almacenamiento de las coordenadas
coordinates = {}
for filename in os.listdir("."):
    if filename.endswith(".csv"):
        df = pd.read_csv(filename)
        coordinates[filename.split(".")[0]] = df.iloc[0].to_dict()

# Procesamiento de cada imagen y etiquetado con las coordenadas correspondientes
labeled_images = []

for filename in os.listdir("."):
    if filename.endswith(".jpg"):
        image_name = os.path.splitext(filename)[0]
        if image_name in coordinates:
            image_path = os.path.join(".", filename)
            coords = coordinates[image_name]

            # Lógica para etiquetar la imagen con las coordenadas usando el modelo de Form Recognizer
            with open(image_path, "rb") as f:
                poller = document_model_admin_client.begin_recognize_custom_forms_from_url(
                    model_id="my-first-model",
                    form_url=f,
                    include_field_elements=True,
                    use_cached_model=False,
                )
                result = poller.result()

            for recognized_form in result:
                print("Form type:", recognized_form.form_type)
                for name, field in recognized_form.fields.items():
                    print("Field '{}' has value '{}' with a confidence score of {}".format(
                        name,
                        field.value,
                        field.confidence
                    ))
                for page in recognized_form.pages:
                    for field in page.page_fields:
                        print("Page field '{}' has value '{}' with a confidence score of {}".format(
                            field.name,
                            field.value,
                            field.confidence
                        ))
                        print("Location:", field.page_number, field.field_elements)

                # Se agrega la imagen etiquetada a la lista de imágenes etiquetadas
                labeled_images.append({"path": image_path, "coordinates": coords})

                # Inicio del proceso de entrenamiento
                poller = document_model_admin_client.begin_build_document_model(
                    build_mode="template",
                    blob_container_url=container_sas_url,
                    model_id="my-first-model",
                    training_files=labeled_images
                )

                # Espera a que el proceso de entrenamiento termine y obtiene el modelo entrenado
                model = poller.result()

                # Realización del test del modelo
                # Ruta de la imagen a analizar
                image_path = "/sysroot/home/andreasandoval/Documentos/BOOTCAMP_F5/OCR/Dataset/Fuente4/parte_amistoso_4_0.jpg" #RUTA

                # Análisis de la imagen
                with open(image_path, "rb") as f:
                    poller = document_model_admin_client.begin_analyze_document(model_id=model.model_id, document=f)
                result = poller.result()

                # Impresión de los resultados en formato JSON
                result_json = json.dumps(result, indent=4)
                print(result_json)

                # Guardar los resultados en un archivo JSON
                with open("resultados.json", "w") as f:
                    json.dump(result, f, indent=4)

                # Guardar el archivo JSON en el disco duro
                with open("result.json", "w") as f:
                    json.dump(result_json, f)