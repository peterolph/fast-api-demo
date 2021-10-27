
from base64 import b64decode
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from io import BytesIO
from PIL import Image

import numpy as np
from tensorflow.keras.applications import densenet
from tensorflow.keras.preprocessing import image as image_preproc

# TODO split this file up a bit

model = densenet.DenseNet121(
  weights="data/densenet121_weights_tf_dim_ordering_tf_kernels.h5"
)

def prep_single_image(image_data):
  # TODO check image_data is valid single image
  resized = image_preproc.smart_resize(
    image_data,
    size=(224, 224))
  input_arr = image_preproc.img_to_array(resized)
  return np.array((input_arr,))

def predict(input_batch):
  preprocessed = densenet.preprocess_input(input_batch)
  predictions = model.predict(preprocessed)
  decoded = densenet.decode_predictions(
    predictions,
    top=1)

  # return the labels (item 1 in tuple) from the top classes from each prediction
  return [pred[0][1] for pred in decoded]

def predict_single_image(image_data):
  return predict(prep_single_image(image_data))[0]

app = FastAPI()

class PredictPayload(BaseModel):
  image: bytes

class PredictResponse(BaseModel):
  response: str

@app.post("/predict", response_model=PredictResponse)
def handle_predict(payload: PredictPayload):
    # TODO check data safety - decompression attacks etc
    # TODO could async be useful here?
    image_data = Image.open(BytesIO(b64decode(payload.image)))
    return PredictResponse(
      response=predict_single_image(image_data))
