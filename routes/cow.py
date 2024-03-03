from typing import List
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument
from models.cow import Cow, Vaccine, dates
from config.db import conn
from schemas.cow import userEntity,usersEntity
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

route = APIRouter()


@route.get('/cows',response_model=List[Cow])
async def findAllUsers():
  cows_from_db = conn.majorproject.cows.find()
  cows = [Cow(**cow) for cow in cows_from_db]
  return cows


@route.post('/cow')
async def create_user(user : Cow):
  conn.majorproject.cows.insert_one(dict(user))

@route.post('/cowvaccine')
async def update_cow_vaccnie(data : Vaccine):
  conn.majorproject.vaccine.insert_one(jsonable_encoder(data))

@route.get('/vaccinedetails', response_model=List[Vaccine])
async def get_vaccine_details():
  vaccines_from_db = conn.majorproject.vaccine.find()
  vaccines = [Vaccine(**vaccine) for vaccine in vaccines_from_db]
  return vaccines

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
  
@route.get('/vaccine/{id}', response_model=Vaccine)
async def get_vaccine_details_by_id(id : str):
  vaccines_from_db = conn.majorproject.vaccine.find_one({"id" : id})
  return vaccines_from_db
  
@route.get("/get-nearby-doctors")
async def get_nearby_doctors(latitude: float, longitude: float):
    
    doctorCollectionObject = conn.majorproject.vetDoctors

    # Replace the following with your actual MongoDB query logic
    doctors_of_db = doctorCollectionObject.aggregate([
        {
            "$project": {
                "_id": 0,
                "Name": 1,
                "Hospital": 1,
                "Specilization": 1,
                "Consultation": 1,
                "Experience": 1,
                "latitude": 1,
                "longitude": 1,
                "distance": {
                    "$add": [
                        {"$pow": [{"$subtract": ["$latitude", latitude]}, 2]},
                        {"$pow": [{"$subtract": ["$longitude", longitude]}, 2]},
                    ]
                },
            }
        },
        {"$sort": {"distance": 1}},
        {"$project": {"_id" : 0}},
    ])

    # Convert the MongoDB cursor to a list of dictionaries
    doctors_list = list(doctors_of_db)

    if not doctors_list:
        raise HTTPException(status_code=404, detail="No nearby doctors found")

    return JSONResponse(content={"message": doctors_list})
