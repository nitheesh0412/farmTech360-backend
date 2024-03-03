from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.cow import route
from routes.scm import scm
from routes.lsd import lsd
app = FastAPI()
origins = [
    "http://localhost:54913",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(route)
app.include_router(scm)
app.include_router(lsd)