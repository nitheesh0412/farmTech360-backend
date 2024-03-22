from typing import List
from pydantic import BaseModel
from datetime import datetime


class Cow(BaseModel):
  id : str
  sex : str
  age : int

class dates(BaseModel):
  date : datetime
  check : str

class Vaccine(BaseModel) :
  id : str
  vaccine_name :str
  doses : int
  timeinterval : int
  status : List[dates] 