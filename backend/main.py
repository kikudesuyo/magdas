from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.ee_index import router as ee_index

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ee_index)
