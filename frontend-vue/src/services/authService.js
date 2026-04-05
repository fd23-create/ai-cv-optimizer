import { useAuth } from '@clerk/clerk-vue'
import api from './api.js'

export const authService = {
  async getToken() {
    const { getToken } = useAuth()
    return await getToken()
  },

  async syncUserWithBackend() {
    try {
      const { user } = useAuth()
      const token = await this.getToken()
      
      const response = await api.post('/api/auth/sync', {
        clerkId: user.value.id,
        email: user.value.primaryEmailAddress.emailAddress,
        firstName: user.value.firstName,
        lastName: user.value.lastName
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      
      return response.data
    } catch (error) {
      console.error('Error syncing user:', error)
      throw error
    }
  },

  async logout() {
    localStorage.removeItem('clerk-db-jwt')
  }
}
