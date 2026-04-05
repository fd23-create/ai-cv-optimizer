import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const isDarkMode = ref(false)
  const sidebarOpen = ref(false)
  const notifications = ref([])
  const modals = ref({
    upload: false,
    settings: false,
    help: false
  })

  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('darkMode', isDarkMode.value)
    document.documentElement.classList.toggle('dark', isDarkMode.value)
  }

  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const showNotification = (message, type = 'info', duration = 5000) => {
    const notification = {
      id: Date.now(),
      message,
      type,
      duration
    }
    
    notifications.value.push(notification)
    
    if (duration > 0) {
      setTimeout(() => {
        removeNotification(notification.id)
      }, duration)
    }
    
    return notification.id
  }

  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const openModal = (modalName) => {
    if (modals.value.hasOwnProperty(modalName)) {
      modals.value[modalName] = true
    }
  }

  const closeModal = (modalName) => {
    if (modals.value.hasOwnProperty(modalName)) {
      modals.value[modalName] = false
    }
  }

  const closeAllModals = () => {
    Object.keys(modals.value).forEach(key => {
      modals.value[key] = false
    })
  }

  const initializeDarkMode = () => {
    const saved = localStorage.getItem('darkMode')
    if (saved !== null) {
      isDarkMode.value = saved === 'true'
    } else {
      isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    document.documentElement.classList.toggle('dark', isDarkMode.value)
  }

  return {
    isDarkMode,
    sidebarOpen,
    notifications,
    modals,
    toggleDarkMode,
    toggleSidebar,
    showNotification,
    removeNotification,
    openModal,
    closeModal,
    closeAllModals,
    initializeDarkMode
  }
})
