from fastapi import FastAPI
from src.routes.plans import plans
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(plans)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cambia según la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
