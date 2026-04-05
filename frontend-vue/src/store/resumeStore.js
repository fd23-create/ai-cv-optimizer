import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { resumeService } from '@/services/resumeService.js'

export const useResumeStore = defineStore('resume', () => {
  const resumes = ref([])
  const currentResume = ref(null)
  const currentAnalysis = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const uploadProgress = ref(0)

  const sortedResumes = computed(() => {
    return [...resumes.value].sort((a, b) => 
      new Date(b.createdAt) - new Date(a.createdAt)
    )
  })

  const uploadResume = async (file) => {
    try {
      isLoading.value = true
      error.value = null
      uploadProgress.value = 0

      const result = await resumeService.uploadResume(file)
      resumes.value.unshift(result.resume)
      currentResume.value = result.resume
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
      uploadProgress.value = 0
    }
  }

  const analyzeResume = async (resumeId) => {
    try {
      isLoading.value = true
      error.value = null

      const result = await resumeService.analyzeResume(resumeId)
      currentAnalysis.value = result.analysis
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const fetchUserResumes = async () => {
    try {
      isLoading.value = true
      error.value = null

      const result = await resumeService.getUserResumes()
      resumes.value = result.resumes
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getResumeById = async (id) => {
    try {
      isLoading.value = true
      error.value = null

      const result = await resumeService.getResumeById(id)
      currentResume.value = result.resume
      
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteResume = async (id) => {
    try {
      isLoading.value = true
      error.value = null

      await resumeService.deleteResume(id)
      resumes.value = resumes.value.filter(r => r.id !== id)
      
      if (currentResume.value?.id === id) {
        currentResume.value = null
        currentAnalysis.value = null
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  const setCurrentResume = (resume) => {
    currentResume.value = resume
  }

  const setCurrentAnalysis = (analysis) => {
    currentAnalysis.value = analysis
  }

  return {
    resumes,
    currentResume,
    currentAnalysis,
    isLoading,
    error,
    uploadProgress,
    sortedResumes,
    uploadResume,
    analyzeResume,
    fetchUserResumes,
    getResumeById,
    deleteResume,
    clearError,
    setCurrentResume,
    setCurrentAnalysis
  }
})
