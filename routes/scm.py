from typing import List
from fastapi import APIRouter, Request
import pickle
import pandas as pd
from config.db import conn
from models.scmModel import SCMModel
from schemas.cow import userEntity,usersEntity
from fastapi.encoders import jsonable_encoder
scm = APIRouter()
model = pickle.load(open("SCMDetection/model.pkl","rb"))
@scm.post('/predict')
async def predictSCM(scmData : Request):
  scmData = await scmData.json()
  data = pd.Series(scmData).to_frame().T    

  query_df = data[['DIM( Days In Milk)', 
                    'Avg(7 days). Daily MY( L )', 
                    'Kg. milk 305 ( Kg )', 
                    'Fat (%)', 
                    'SNF (%)', 
                    'Density ( Kg/ m3', 
                    'Protein (%)',
                    'Conductivity (mS/cm)',
                    'pH',
                    'Freezing point (⁰C)',
                    'Salt (%)',
                    'Lactose (%)']]

  prediction = model.predict(query_df)
  return {"prediction": prediction.tolist()}