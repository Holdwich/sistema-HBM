from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from api.endpoints import measurements, irregularities, simulation

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servidor HBM+")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(measurements.router)
app.include_router(irregularities.router)
app.include_router(simulation.router)

@app.get("/")
async def redirect_to_docs():
    return ({"message": "Acesse a documentação em /docs"})
