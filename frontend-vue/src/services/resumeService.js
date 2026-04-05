import api from './api.js'

export const resumeService = {
  async uploadResume(file) {
    const formData = new FormData()
    formData.append('resume', file)
    
    const response = await api.post('/api/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  async getResumeById(id) {
    const response = await api.get(`/api/resumes/${id}`)
    return response.data
  },

  async getUserResumes() {
    const response = await api.get('/api/resumes/user')
    return response.data
  },

  async deleteResume(id) {
    const response = await api.delete(`/api/resumes/${id}`)
    return response.data
  },

  async analyzeResume(resumeId) {
    const response = await api.post(`/api/resumes/${resumeId}/analyze`)
    return response.data
  },

  async getAnalysisResult(analysisId) {
    const response = await api.get(`/api/analysis/${analysisId}`)
    return response.data
  }
}
