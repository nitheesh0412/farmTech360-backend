# from typing import List
from pydantic import BaseModel

class SCMModel(BaseModel):
  DIM: int
  Daily_MY: int
  Kg_milk: int
  Fat: float
  SNF: float
  Density: int
  Protein: float
  Conductivity: int
  pH: float
  Freezing: float
  Salt: float
  Lactose: float