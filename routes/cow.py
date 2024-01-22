from typing import List
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from models.cow import Cow, Vaccine, dates
from config.db import conn
from schemas.cow import userEntity,usersEntity
from fastapi.encoders import jsonable_encoder
route = APIRouter()

@route.get('/cows',response_model=List[Cow])
async def findAllUsers():
  return conn.majorproject.cows.find()


@route.post('/cow')
async def create_user(user : Cow):
  conn.majorproject.cows.insert_one(dict(user))

@route.post('/cowvaccine')
async def update_cow_vaccnie(data : Vaccine):
  conn.majorproject.vaccine.insert_one(jsonable_encoder(data))

@route.get('/vaccinedetails', response_model=List[Vaccine])
async def get_vaccine_details():
  return conn.majorproject.vaccine.find()

@route.put('/vaccinedetails/{id}', response_model=Vaccine)
async def get_vaccine_details(id : str,body : dates):
  update = {
      '$push': {'status': dict(body)}
  }
  res =   conn.majorproject.vaccine.find_one_and_update(
    {"id" : id},
    update,
    return_document=ReturnDocument.AFTER
  )
  if res:
    return res
  else:
    raise HTTPException(status_code=404, detail="Item not found")