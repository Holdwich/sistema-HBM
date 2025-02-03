from typing import List, Optional
from sqlalchemy.orm import Session
from models.irregularity import Irregularity
from datetime import datetime

class IrregularityRepository:
    """
    Responsável pela persistência das irregularidades.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, irregularity: Irregularity) -> Irregularity:
        """
        Cria e adiciona uma nova irregularidade ao banco de dados.

        Args:
            irregularity (Irregularity): A irregularidade a ser adicionada.

        Returns:
            Irregularity: A irregularidade adicionada com seu ID atualizado.
        """
        self.db.add(irregularity)
        self.db.commit()
        self.db.refresh(irregularity)
        return irregularity

    def get_active(self, device_id: str) -> Optional[Irregularity]:
        """
        Obtém a irregularidade ativa para um dispositivo específico.

        Args:
            device_id (str): Identificador do dispositivo.

        Returns:
            Optional[Irregularity]: A irregularidade ativa, se existir, caso contrário, None.
        """
        return (
            self.db.query(Irregularity)
            .filter(Irregularity.device_id == device_id, Irregularity.end_timestamp.is_(None))
            .first()
        )

    def close_irregularity(self, irregularity: Irregularity) -> Irregularity:
        """
        Fecha uma irregularidade atualizando seu timestamp de término.

        Args:
            irregularity (Irregularity): A irregularidade a ser fechada.

        Returns:
            Irregularity: A irregularidade fechada com o timestamp de término atualizado.
        """
        irregularity.end_timestamp = datetime.now()
        self.db.commit()
        self.db.refresh(irregularity)
        return irregularity

    def get_all(self, device_id: str) -> List[Irregularity]:
        """
        Retorna todas as irregularidades de um dispositivo específico ordenadas por timestamp de início.

        Args:
            device_id (str): Identificador do dispositivo.

        Returns:
            List[Irregularity]: Lista de todas as irregularidades associadas ao dispositivo.
        """
        return (
            self.db.query(Irregularity)
            .filter(Irregularity.device_id == device_id)
            .order_by(Irregularity.start_timestamp)
            .all()
        )