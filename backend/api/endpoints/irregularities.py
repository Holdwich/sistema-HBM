# backend/api/endpoints/irregularities.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.deps import get_db
from schemas.irregularity import IrregularityResponse
from repos.irregularityRepository import IrregularityRepository

router = APIRouter(prefix="/api", tags=["Irregularidades"])

@router.get("/irregularities", response_model=list[IrregularityResponse])
def get_irregularities(device_id: str = Query(...), db: Session = Depends(get_db)):
    """
    Retorna todas as irregularidades para um dispositivo específico.

    Args:
        device_id: Identificador do dispositivo para o qual as irregularidades devem ser recuperadas.

    Returns:
        list[IrregularityResponse]: Lista de irregularidades registradas pelo dispositivo.
    """
    irregularity_repo = IrregularityRepository(db)
    irregularities = irregularity_repo.get_all(device_id)
    return irregularities
