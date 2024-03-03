
from fastapi import APIRouter
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
lsd = APIRouter()
loaded_best_model = keras.models.load_model("./LSDDetection/Notebooks/model_05-0.92.h5")
labels = {0: 'Lumpy Skin', 1: 'Normal Skin'}

def predict(img):
    img = image.img_to_array(img, dtype=np.uint8)

    img = np.array(img) / 255.0

    p = loaded_best_model.predict(img[np.newaxis, ...])

    predicted_class = labels[np.argmax(p[0], axis=-1)]
    
    return predicted_class

@lsd.post("/predict")
async def predict_skin_condition(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))

        img = img.resize((256, 256))

        predicted_class = predict(img)

        return JSONResponse(content={"predicted_class": predicted_class}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)