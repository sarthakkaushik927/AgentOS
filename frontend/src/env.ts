const envUrl = import.meta.env.VITE_API_BASE_URL
let baseUrl = envUrl ? envUrl.replace(/\/+$/, '') : 'http://localhost:8000/api/v1'

if (baseUrl && !baseUrl.endsWith('/api/v1')) {
  baseUrl += '/api/v1'
}

export const API_BASE_URL = baseUrl
