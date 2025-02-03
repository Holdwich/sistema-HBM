import asyncio
import random
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from api.deps import get_db
from repos.measurementRepository import MeasurementRepository
from repos.irregularityRepository import IrregularityRepository
from services.measurementService import MeasurementService
from utils.simulation import generate_baseline

router = APIRouter(prefix="/api", tags=["Simulações"])

@router.post("/simulate")
async def simulate(
    device_id: str,
    mode: str = Query("normal", description="Opções: normal, anormal, misto"),
    count: int = Query(100, description="Quantidade de medições a enviar"),
    interval: int = Query(15, description="Intervalo das medições em ms"),
    db: Session = Depends(get_db)
):
    """
    Simula medições de um dispositivo com diferentes modos de simulação diretamente na API.

    Modos possíveis:
    - normal: as medições seguem a curva de baseline
    - anormal: as medições seguem a curva de baseline, mas com um desvio de 30%
    - misto: as medições seguem a curva de baseline, mas com um desvio de 30% em algumas delas

    A simulação pode ser configurada com parâmetros:
    - device_id: o id do dispositivo a ser simulado
    - mode: o modo de simulação (padrão: normal)
    - count: a quantidade de medições a serem geradas (padrão: 100)
    - interval: o intervalo das medições em milissegundos (padrão: 15)

    Retorna uma lista de medições simuladas.
    """
    measurement_repo = MeasurementRepository(db)
    irregularity_repo = IrregularityRepository(db)
    service = MeasurementService(measurement_repo, irregularity_repo)

    results = []
    for i in range(count):
        time_ms = interval
        baseline = generate_baseline(time_ms)
        value = baseline

        if mode == "anormal":
            value = baseline * 1.3
        elif mode == "misto":
            if random.random() < 0.2:
                value = baseline * 1.3

        alert_result = service.process_measurement(device_id, time_ms, value)

        results.append({
            "time_ms": time_ms,
            "value": value,
            "alert": alert_result["alert"]
        })
        await asyncio.sleep(interval / 1000)
    return {"device_id": device_id, "simulated_measurements": results}
