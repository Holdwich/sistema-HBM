'use client';
import { useState } from 'react';
import { registerMeasurement, simulateMeasurements, getMeasurementsHistory, getIrregularities } from '../services/api';

export default function Home() {
  const [deviceId, setDeviceId] = useState('');
  const [mode, setMode] = useState('normal');
  const [count, setCount] = useState(60);
  const [value, setValue] = useState(0);
  const [intervalMs, setIntervalMs] = useState(50);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [irregularities, setIrregularities] = useState([]);
  const [error, setError] = useState('');

  const handleRegisterMeasurement = async () => {
    setError('');
    if (!deviceId) {
      setError('Informe o ID do dispositivo.');
      return;
    }
    if (value < 0) {
      setError('Informe um valor personalizado válido.');
      return;
    }
    setIrregularities([]);
    setHistory([]);
    console.log(value);
    try {
      const response = await registerMeasurement({
        device_id: deviceId,
        time_ms: intervalMs,
        value: value,
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('Erro ao registrar medição.');
    }
  }

  const handleSimulate = async () => {
    setError('');
    if (!deviceId) {
      setError('Informe o ID do dispositivo.');
      return;
    }
    setIrregularities([]);
    setHistory([]);
    try {
      const response = await simulateMeasurements({
        device_id: deviceId,
        mode: mode,
        count: count,
        interval: intervalMs
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError('Erro ao simular medições.');
    }
  };

  const fetchHistory = async () => {
    setError('');
    if (!deviceId) {
      setError('Informe o ID do dispositivo.');
      return;
    }
    setIrregularities([]);
    setResult(null);
    try {
      const response = await getMeasurementsHistory(deviceId);
      setHistory(response.data);
    } catch (err) {
      console.error(err);
      setError('Erro ao buscar histórico de medições.');
    }
  };

  const fetchIrregularities = async () => {
    setError('');
    if (!deviceId) {
      setError('Informe o ID do dispositivo.');
      return;
    }
    setResult(null);
    setHistory([]);
    try {
      const response = await getIrregularities(deviceId);
      setIrregularities(response.data);
    } catch (err) {
      console.error(err);
      setError('Erro ao buscar irregularidades.');
    }
  };

  return (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <div style={{ padding: '2rem'}}>
        <h1>Simulador HBM+</h1>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            ID do dispositivo: 
            <input
              type="text"
              value={deviceId}
              onChange={(e) => setDeviceId(e.target.value)}
              style={{ marginLeft: '0.5rem' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            Modo de simulação:
            <select value={mode} onChange={(e) => setMode(e.target.value)} style={{ marginLeft: '0.5rem' }}>
              <option value="normal">Normal</option>
              <option value="anormal">Anormal</option>
              <option value="misto">Misto</option>
            </select>
          </label>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            Mediçōes (N):
            <input
              type="number"
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
              style={{ marginLeft: '0.5rem', width: '80px' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            Valor de medição personalizado (maior que 0):
            <input
              type="number"
              step="0.01"
              value={value}
              onChange={(e) => setValue(Number(e.target.value))}
              style={{ marginLeft: '0.5rem', width: '80px' }}
            />
          </label>
        </div>
        <div style={{ marginBottom: '1rem' }}>
          <label>
            Intervalo de tempo das medições (ms):
            <input
              type="number"
              value={intervalMs}
              onChange={(e) => setIntervalMs(Number(e.target.value))}
              style={{ marginLeft: '0.5rem', width: '80px' }}
            />
          </label>
        </div>
        <button onClick={handleRegisterMeasurement} style={{ marginRight: '1rem' }}>
          Simular Medição Individual (Valor personalizado)
        </button>
        <button onClick={handleSimulate} style={{ marginRight: '1rem' }}>
          Simular Mediçōes
        </button>
        <button onClick={fetchHistory} style={{ marginRight: '1rem' }}>
          Histórico de Mediçōes
        </button>
        <button onClick={fetchIrregularities}>
          Irregularidades
        </button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && (
          <div style={{ marginTop: '2rem' }}>
            <h2>Resultados da Simulação</h2>
            <p>ID do dispositivo: {result.device_id}</p>
            <ul>
              {result.simulated_measurements ? (
                result.simulated_measurements.map((m, index) => (
                  <li key={index}>
                    {`Tempo: ${m.time_ms} ms, Valor: ${m.value.toFixed(2)}, Alerta: ${m.alert || '-'}`}
                  </li>
                ))
              ) : (
                <li>{`Tempo: ${result.time_ms} ms, Valor: ${result.value.toFixed(2)}, Alerta: ${result.alert || '-'}`}</li>
              )}
            </ul>
          </div>
        )}
        {history.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h2>Histórico de Mediçōes</h2>
            <ul>
              {history.map((m) => (
                <li key={m.id}>
                  {`[${new Date(m.timestamp).toLocaleString()}] Tempo: ${m.time_ms} ms, Valor: ${m.value}`}
                </li>
              ))}
            </ul>
          </div>
        )}
        {irregularities.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h2>Irregularidades</h2>
            <ul>
              {irregularities.map((irreg) => (
                <li key={irreg.id}>
                  {`Início: ${new Date(irreg.start_timestamp).toLocaleString()} - Fim: ${
                    irreg.end_timestamp ? new Date(irreg.end_timestamp).toLocaleString() : 'Ativa'
                  }`}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div>
        <p>Para usar o simulador, siga as instruções abaixo:</p>
        <ol>
          <li>Insira o ID do dispositivo no campo apropriado.</li>
          <li>Escolha o modo de simulação entre Normal, Anormal ou Misto.</li>
          <li>Defina o número de medições desejado (N).</li>
          <li>Se necessário, insira um valor de medição personalizado (Aplicável somente para medição única).</li>
          <li>Determine o intervalo de tempo das medições em milissegundos.</li>
          <li>Clique em "Simular Medição Individual" para uma medição única ou "Simular Mediçōes" para múltiplas medições com os parâmetros especificados.</li>
          <li>Use os botões apropriados para visualizar o histórico de medições (últimos 30 dias) ou irregularidades detectadas.</li>
        </ol>
      </div>
    </div>
  );
}
