import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // URL do backend FastAPI
  headers: {
    'Content-Type': 'application/json'
  }
});

export const registerMeasurement = (params) => {
    return apiClient.post('/measurements', null, { params });
};

export const simulateMeasurements = (params) => {
  return apiClient.post('/simulate', null, { params });
};

export const getMeasurementsHistory = (device_id) => {
  return apiClient.get('/measurements/history', { params: { device_id } });
};

export const getIrregularities = (device_id) => {
  return apiClient.get('/irregularities', { params: { device_id } });
};
