import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuth } from '@clerk/clerk-vue'
import { authService } from '@/services/authService.js'

export const useAuthStore = defineStore('auth', () => {
  const { isSignedIn, user } = useAuth()
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => isSignedIn.value)
  const currentUser = computed(() => user.value)

  const syncUser = async () => {
    if (!isSignedIn.value) return
    
    try {
      isLoading.value = true
      error.value = null
      await authService.syncUserWithBackend()
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    isLoading,
    error,
    isAuthenticated,
    currentUser,
    syncUser,
    logout,
    clearError
  }
})
