from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pdf2image import convert_from_bytes
from google.cloud import vision
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure ton chemin vers la clé JSON Google via variable d'environnement
# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
# Ou charge ta clé API dans ton code (moins sécurisé)

client = vision.ImageAnnotatorClient()

def ocr_with_google(image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""

@app.post("/ocr/extract")
async def extract_cotisations(pdf: UploadFile = File(...)):
    content = await pdf.read()
    images = convert_from_bytes(content)

    full_text = ""
    for image in images:
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        image_bytes = buf.getvalue()

        ocr_text = ocr_with_google(image_bytes)
        full_text += ocr_text + "\n"

    # Ici, tu peux appliquer un parsing similaire à celui précédent sur full_text
    # pour extraire les cotisations annuelles, mensualisées et les totaux.
    # Par exemple, réutilise parse_cotisations_table(full_text)

    # Extrait fictif pour exemple:
    # return {"extracted_text": full_text}

    # Implémentation du parsing selon ton besoin ici ...

    return {"extracted_text": full_text}
