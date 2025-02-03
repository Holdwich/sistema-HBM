import math
import datetime
from models.measurement import Measurement
from models.irregularity import Irregularity
from repos.measurementRepository import MeasurementRepository
from repos.irregularityRepository import IrregularityRepository

class MeasurementService:
    def __init__(self, measurement_repo: MeasurementRepository, irregularity_repo: IrregularityRepository):
        """
        Inicializa o serviço de medições com os repositórios necessários.

        Args:
            measurement_repo (MeasurementRepository): Repositório de medições.
            irregularity_repo (IrregularityRepository): Repositório de irregularidades.
        """
        self.measurement_repo = measurement_repo
        self.irregularity_repo = irregularity_repo

    @staticmethod
    def compute_baseline(time_ms: int) -> float:
        """
        Calcula o valor baseline com a fórmula:
        Y = -0.06366 + 0.12613 cos(pi * x/500) + 0.12258 cos(pi * x/250)
            + 0.01593 sin(pi * x/500) + 0.03147 sin(pi * x/250)

        Args:
            time_ms (int): O tempo em milissegundos para o qual se deseja calcular o baseline.

        Returns:
            float: O valor baseline.
        """
        x = time_ms
        y = (-0.06366 +
             0.12613 * (math.cos(math.pi * x / 500)) +
             0.12258 * (math.cos(math.pi * x / 250)) +
             0.01593 * (math.sin(math.pi * x / 500)) +
             0.03147 * (math.sin(math.pi * x / 250)))
        return y

    @staticmethod
    def is_abnormal(measured: float, baseline: float) -> bool:
        """
        Verifica se a medição desvia 20% ou mais do baseline.
        
        Args:
            measured (float): A medição a ser verificada.
            baseline (float): O baseline.
        
        Returns:
            bool: True se a medição desviar 20% ou mais do baseline, False caso contrário.
        """
        if baseline == 0:
            return abs(measured - baseline) >= 0.2
        return abs(measured - baseline) / abs(baseline) >= 0.2

    def process_measurement(self, device_id: str, time_ms: int, value: float) -> dict:
        """
        Registra a medição, verifica as últimas 60 medições e decide se envia 'bip' ou 'bipbip' (caso aplicável).
        
        Args:
            device_id (str): O ID do dispositivo.
            time_ms (int): O intervalo em milissegundos da medição para usar no cálculo da baseline.
            value (float): O valor da medição.
        
        Returns:
            dict: Um dicionário contendo a chave "alert" com o valor "bip" ou "bipbip" (caso aplicável),
            e a chave "abnormal_count" com o número de medições anormais nas últimas 60 mediçöes.
        """
        measurement = Measurement(device_id=device_id, time_ms=time_ms, value=value)
        self.measurement_repo.create(measurement)

        last_measurements = self.measurement_repo.get_last_n(device_id, 60)
        abnormal_count = 0
        for m in last_measurements:
            baseline = self.compute_baseline(m.time_ms)
            if self.is_abnormal(m.value, baseline):
                abnormal_count += 1

        alert = None
        active_irreg = self.irregularity_repo.get_active(device_id)

        if abnormal_count >= 5 and active_irreg is None:
            new_irreg = Irregularity(device_id=device_id, start_timestamp=datetime.datetime.now())
            self.irregularity_repo.create(new_irreg)
            alert = "bip"  # sinal de emergência
        elif abnormal_count == 0 and active_irreg is not None:
            measurements_since_irreg = [
                m for m in self.measurement_repo.get_last_n(device_id, 100)
                if m.timestamp >= active_irreg.start_timestamp
            ]
            if len(measurements_since_irreg) >= 60:
                self.irregularity_repo.close_irregularity(active_irreg)
                alert = "bipbip" # fecha emergência
        return {"alert": alert, "abnormal_count": abnormal_count}
