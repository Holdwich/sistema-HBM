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

@router.post("/measurements")
def add_measurement(device_id: str = Query(...), time_ms: int = Query(...), value: float = Query(...), db: Session = Depends(get_db)):
    """Adiciona uma medição ao banco de dados e processa a irregularidade se necessário.

    Args:
        device_id (str): O ID do dispositivo que fez a medição,
        time_ms (int): O tempo em milissegundos da medição,
        value (float): O valor da medição

    Returns:
        list[]: A medição adicionada, e uma mensagem de alerta, se houver
    """
    
    measurement_repo = MeasurementRepository(db)
    irregularity_repo = IrregularityRepository(db)
    service = MeasurementService(measurement_repo, irregularity_repo)

    # Processa a medição (incluindo verificação de irregularidades)
    result = service.process_measurement(device_id, time_ms, value)

    return {"device_id" : device_id, "time_ms": time_ms, "value": value, "alert": result["alert"]}

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
