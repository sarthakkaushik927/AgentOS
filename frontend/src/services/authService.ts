import { apiClient } from './apiClient'
import type { AuthTokens, User } from '../types/auth'

export const authService = {
  login: async (email: string, password: string): Promise<AuthTokens> => {
    const params = new URLSearchParams()
    params.append('username', email)
    params.append('password', password)
    
    return apiClient.post('/auth/login', params)
  },

  register: async (email: string, password: string): Promise<User> => {
    return apiClient.post('/auth/register', { email, password })
  },

  getMe: async (): Promise<User> => {
    return apiClient.get('/users/me')
  }
}
