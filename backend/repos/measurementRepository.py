from typing import List
from sqlalchemy.orm import Session
from models.measurement import Measurement
from datetime import datetime, timedelta

class MeasurementRepository:
    """
    Responsável pela persistência das medições.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, measurement: Measurement) -> Measurement:
        """
        Adiciona uma nova medição à base de dados.
        
        Args:
            measurement (Measurement): A medição a ser adicionada.
        
        Returns:
            Measurement: A medição adicionada.
        """
        self.db.add(measurement)
        self.db.commit()
        self.db.refresh(measurement)
        return measurement

    def get_last_n(self, device_id: str, n: int) -> List[Measurement]:
        """
        Obtém as últimas N medições de um dispositivo.
        
        Args:
            device_id (str): O ID do dispositivo.
            n (int): O número de medições a obter.
        
        Returns:
            List[Measurement]: A lista de medições do dispositivo.
        """
        return (
            self.db.query(Measurement)
            .filter(Measurement.device_id == device_id)
            .order_by(Measurement.timestamp.desc())
            .limit(n)
            .all()
        )

    def get_history(self, device_id: str, days: int = 30) -> List[Measurement]:
        """
        Obtém o histórico de medições de um dispositivo com base na quantidade de dias.
        
        Args:
            device_id (str): O ID do dispositivo.
            days (int): O número de dias a obter (padrão 30).
        
        Returns:
            List[Measurement]: A lista de medições do dispositivo.
        """
        since = datetime.now() - timedelta(days=days)
        return (
            self.db.query(Measurement)
            .filter(Measurement.device_id == device_id, Measurement.timestamp >= since)
            .order_by(Measurement.timestamp)
            .all()
        )