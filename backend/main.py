from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
import time
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

import numpy as np
from PIL import Image
from io import BytesIO
import os
from process.model.main import process

app = FastAPI()

origins = [
    "file:///D:/dead/ir-proj/src/frontend/index.html",
    "http://127.0.0.1:5500",
    "localhost:5500",
    "http://localhost:3000",
    "127.0.0.1:5500",
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/data',StaticFiles(directory="data"))

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to Image Retrieval Engine."}


def load_image_into_numpy_array(data):
    return np.array(Image.open(BytesIO(data)))


@app.post("/search", tags=["search"])
async def search_image(
    image: UploadFile = File(...),
    x1: int = Body(0),
    x2: int = Body(0),
    y1: int = Body(0),
    y2: int = Body(0)
    ):
    print("hello ", x1, x2, y1, y2)
    data = load_image_into_numpy_array(await image.read())
    data = data[y1:y2+1, x1:x2+1, :]
    topK = process(data)

    print("np: ", data.shape)
    # return "image " + str(data.shape) \
    #         + ", coor: (" + str(x1) + ", " + str(y1) \
    #         + "), ("  + str(x2) + ", " + str(y2) + ")" 
    return topK
