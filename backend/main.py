from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import time
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

import numpy as np
from PIL import Image
from io import BytesIO
import os
from process.model.main import process, initialize
import cv2
import configparser

app = FastAPI()

origins = [
    "file:///D:/dead/ir-proj/src/frontend/index.html",
    "http://127.0.0.1:5500",
    "localhost:5500",
    "http://localhost:3000",
    "127.0.0.1:5500",
    "*"
]

config = configparser.ConfigParser()
config.read('config.ini')
model=config['config']['model']
model=int(model)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/data',StaticFiles(directory="data"))

print('Initializing model',model)
initialize(type_model=model)

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Image Retrieval Engine."}


def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)).convert('RGB'))


@app.post("/search", tags=["search"])
async def search_image(
    image: UploadFile = File(...),
    x1: int = Body(0),
    x2: int = Body(0),
    y1: int = Body(0),
    y2: int = Body(0)
    ):
    print("hello ", x1, x2, y1, y2)
    # data = load_image_into_numpy_array(await image.read())
    # Convert to cv2 bgr format
    # data = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
    data = Image.open(BytesIO(await image.read())).convert('RGB')
    if not(x1==0 and x2==0 and y1==0 and y2==0):
        # data = data[y1:y2+1, x1:x2+1, :]
        data = data.crop((x1,y1,x2,y2))
    topK = process(data)
    # Chỉ thêm jpg vào để frontend trả về thôi
    topK = [x + ".jpg" for x in topK]

    # return "image " + str(data.shape) \
    #         + ", coor: (" + str(x1) + ", " + str(y1) \
    #         + "), ("  + str(x2) + ", " + str(y2) + ")" 
    return topK
