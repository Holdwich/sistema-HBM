from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from api.endpoints import measurements, irregularities, simulation

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servidor HBM+")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

app.include_router(measurements.router)
app.include_router(irregularities.router)
app.include_router(simulation.router)
