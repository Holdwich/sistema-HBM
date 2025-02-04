from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_register_measurement():
    """
    Testa o endpoint de registro de medições.

    Envia uma requisição POST para o endpoint "/measurements" com dados de medição.
    Verifica se a resposta tem status 200 e se os dados retornados contêm o 
    device_id, time_ms corretos e um campo de timestamp.
    """
    
    # Dados para registrar uma medição
    data = {
        "device_id": "test-device",
        "time_ms": 50,
        "value": 0.2
    }
    response = client.post("/measurements", json=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["device_id"] == data["device_id"]
    assert json_data["time_ms"] == data["time_ms"]
    # Verifica se a medição possui um timestamp gerado
    assert "timestamp" in json_data

def test_get_measurements_history():
    """
    Testa o endpoint de histórico de medições para um dispositivo específico.

    Envia uma requisição GET para o endpoint "/measurements/history" usando um
    device_id específico e verifica se a resposta tem status 200. 
    Confirma se os dados retornados são uma lista, que pode estar vazia.
    """
 
    # Utiliza o mesmo device_id do teste anterior para recuperar o histórico
    device_id = "test-device"
    response = client.get("/measurements/history", params={"device_id": device_id})
    assert response.status_code == 200
    json_data = response.json()
    # O retorno deve ser uma lista (mesmo que vazia)
    assert isinstance(json_data, list)

def test_simulate_endpoint():
    """
    Testa o endpoint de simulação com 10 medições.

    Envia uma requisição POST para o endpoint "/simulate" com parâmetros de
    simulação (device_id, mode, count, interval) e verifica se a resposta tem
    status 200. Confirma se os dados retornados contêm o device_id correto e
    uma lista de medições simuladas com o tamanho correto.
    """
    # Testa o endpoint de simulação com 10 medições
    params = {
        "device_id": "simulate-device",
        "mode": "normal",
        "count": 10,
        "interval": 50
    }
    response = client.post("/simulate", params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data.get("device_id") == params["device_id"]
    measurements = json_data.get("simulated_measurements")
    assert isinstance(measurements, list)
    assert len(measurements) == params["count"]

def test_get_irregularities():
    """
    Testa o endpoint de irregularidades para um dispositivo específico.

    Envia uma requisição GET para o endpoint "/irregularities" com um device_id
    específico e verifica se a resposta tem status 200. Confirma se os dados
    retornados são uma lista, que pode estar vazia.
    """

    # Testa o endpoint de irregularidades para um device específico
    device_id = "test-device"
    response = client.get("/irregularities", params={"device_id": device_id})
    assert response.status_code == 200
    json_data = response.json()
    # O retorno deve ser uma lista (mesmo que vazia)
    assert isinstance(json_data, list)