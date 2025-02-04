import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // URL do backend FastAPI
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Registra uma nova medição no banco de dados da nuvem.
 *
 * @param {Object} params
 * @param {string} params.device_id - O ID do dispositivo.
 * @param {number} params.time_ms - O tempo em milissegundos da medição.
 * @param {number} params.value - O valor da medição.
 *
 * @return {Promise<AxiosResponse>} - Uma promessa que resolve com a resposta do servidor.
 */

export const registerMeasurement = (params) => {
    return apiClient.post('/measurements', null, { params });
};

/**
 * Simula medições de um dispositivo com base nos parâmetros fornecidos.
 *
 * @param {Object} params - Os parâmetros para a simulação.
 * @param {string} params.device_id - O ID do dispositivo a ser simulado.
 * @param {string} [params.mode="normal"] - O modo de simulação. Opções: "normal", "anormal", "misto".
 * @param {number} [params.count=100] - A quantidade de medições a serem geradas.
 * @param {number} [params.interval=15] - O intervalo das medições em milissegundos.
 *
 * @return {Promise<AxiosResponse>} - Uma promessa que resolve com a resposta do servidor contendo as medições simuladas.
 */

export const simulateMeasurements = (params) => {
  return apiClient.post('/simulate', null, { params });
};

/**
 * Busca o histórico de medições de um dispositivo.
 *
 * @param {string} device_id - O ID do dispositivo.
 *
 * @return {Promise<AxiosResponse>} - Uma promessa que resolve com a resposta do servidor contendo o histórico de medições.
 */

export const getMeasurementsHistory = (device_id) => {
  return apiClient.get('/measurements/history', { params: { device_id } });
};

/**
 * Busca as irregularidades de um dispositivo.
 *
 * @param {string} device_id - O ID do dispositivo.
 *
 * @return {Promise<AxiosResponse>} - Uma promessa que resolve com a resposta do servidor contendo as irregularidades do dispositivo.
 */

export const getIrregularities = (device_id) => {
  return apiClient.get('/irregularities', { params: { device_id } });
};
