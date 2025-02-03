# backend/api/endpoints/measurements.py
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.measurement import MeasurementRequest, MeasurementResponse
from repos.measurementRepository import MeasurementRepository
from repos.irregularityRepository import IrregularityRepository
from services.measurementService import MeasurementService
from models.measurement import Measurement

router = APIRouter(prefix="/api", tags=["Medições"])

@router.post("/measurements", response_model=MeasurementResponse)
def add_measurement(measurement: MeasurementRequest, db: Session = Depends(get_db)):
    """Adiciona uma medição ao banco de dados e processa a irregularidade se necessário.

    Args:
        measurement (MeasurementRequest): A medição a ser adicionada

    Returns:
        MeasurementResponse: A medição adicionada
    """
    
    measurement_repo = MeasurementRepository(db)
    irregularity_repo = IrregularityRepository(db)
    service = MeasurementService(measurement_repo, irregularity_repo)

    # Processa a medição (incluindo verificação de irregularidades)
    result = service.process_measurement(measurement.device_id, measurement.time_ms, measurement.value)
    
    if result["alert"]:

        Response.headers["X-Alert"] = result["alert"]

    return measurement_repo.create(Measurement(
        device_id=measurement.device_id,
        time_ms=measurement.time_ms,
        value=measurement.value
    )), Response

@router.get("/measurements/history", response_model=list[MeasurementResponse])
def get_history(device_id: str = Query(...), db: Session = Depends(get_db)):
    """Obtém o histórico de medições de um dispositivo. (Últimos 30 dias)

    Args:
        device_id (str): O ID do dispositivo.

    Returns:
        list[MeasurementResponse]: A lista de medições do dispositivo.
    """
    measurement_repo = MeasurementRepository(db)
    history = measurement_repo.get_history(device_id)
    return history
