from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os 

print(os.getcwd())

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = joblib.load("models/whole_pipeline_svr.pkl")


class InputData(BaseModel):
    features: list[float]


@app.post("/predict")
async def predict(data: InputData):
    return {"remark": {pipeline.predict([data.features])[0]}}
