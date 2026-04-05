<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Tableau de bord</h1>
      <div class="header-actions">
        <button @click="refreshData" class="refresh-btn" :disabled="isLoading">
          <RefreshCw :class="{ 'animate-spin': isLoading }" />
          Actualiser
        </button>
        <UploadButton
          @file-selected="handleUpload"
          @success="handleUploadSuccess"
          :is-loading="isUploading"
          button-text="Nouveau CV"
        />
      </div>
    </div>

    <!-- Stats Overview -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <FileText />
        </div>
        <div class="stat-content">
          <h3>{{ stats.totalResumes }}</h3>
          <p>CV analysés</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <TrendingUp />
        </div>
        <div class="stat-content">
          <h3>{{ stats.averageScore }}%</h3>
          <p>Score moyen</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <Calendar />
        </div>
        <div class="stat-content">
          <h3>{{ stats.thisMonth }}</h3>
          <p>Ce mois-ci</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <Award />
        </div>
        <div class="stat-content">
          <h3>{{ stats.bestScore }}%</h3>
          <p>Meilleur score</p>
        </div>
      </div>
    </div>

    <!-- Recent Resumes -->
    <div class="recent-section">
      <div class="section-header">
        <h2>CV récents</h2>
        <div class="filter-tabs">
          <button
            v-for="tab in filterTabs"
            :key="tab.value"
            @click="activeFilter = tab.value"
            class="filter-tab"
            :class="{ 'filter-tab--active': activeFilter === tab.value }"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <div v-if="filteredResumes.length === 0" class="empty-state">
        <div class="empty-icon">
          <FileText />
        </div>
        <h3>Aucun CV trouvé</h3>
        <p>Commencez par télécharger votre premier CV</p>
        <UploadButton
          @file-selected="handleUpload"
          button-text="Télécharger un CV"
        />
      </div>

      <div v-else class="resumes-grid">
        <div
          v-for="resume in filteredResumes"
          :key="resume.id"
          class="resume-card"
          @click="selectResume(resume)"
        >
          <div class="resume-header">
            <div class="resume-info">
              <h3>{{ resume.originalName }}</h3>
              <p>{{ formatDate(resume.createdAt) }}</p>
            </div>
            <div class="resume-score" :class="getScoreClass(resume.score)">
              {{ resume.score }}%
            </div>
          </div>
          
          <div class="resume-preview">
            <div class="preview-content">
              <div class="preview-item">
                <span class="preview-label">Compétences:</span>
                <span class="preview-value">{{ resume.skillsCount || 0 }}</span>
              </div>
              <div class="preview-item">
                <span class="preview-label">Expériences:</span>
                <span class="preview-value">{{ resume.experienceCount || 0 }}</span>
              </div>
              <div class="preview-item">
                <span class="preview-label">Formation:</span>
                <span class="preview-value">{{ resume.educationCount || 0 }}</span>
              </div>
            </div>
          </div>
          
          <div class="resume-actions">
            <button @click.stop="viewAnalysis(resume)" class="action-btn primary">
              <Eye />
              Voir l'analyse
            </button>
            <button @click.stop="downloadResume(resume)" class="action-btn secondary">
              <Download />
              Télécharger
            </button>
            <button @click.stop="deleteResume(resume)" class="action-btn danger">
              <Trash2 />
              Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Chart -->
    <div class="chart-section">
      <h2>Progression des scores</h2>
      <div class="chart-container">
        <canvas ref="progressChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useResumeStore } from '@/store/resumeStore.js'
import { useUIStore } from '@/store/uiStore.js'
import { formatters } from '@/utils/formatters.js'
import UploadButton from '@/components/UploadButton.vue'
import {
  RefreshCw,
  FileText,
  TrendingUp,
  Calendar,
  Award,
  Eye,
  Download,
  Trash2
} from 'lucide-vue-next'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const router = useRouter()
const resumeStore = useResumeStore()
const uiStore = useUIStore()

const progressChart = ref(null)
const chartInstance = ref(null)
const isLoading = ref(false)
const isUploading = ref(false)
const activeFilter = ref('all')

const filterTabs = [
  { label: 'Tous', value: 'all' },
  { label: 'Excellents', value: 'excellent' },
  { label: 'Bons', value: 'good' },
  { label: 'Moyens', value: 'average' },
  { label: 'Faibles', value: 'poor' }
]

const stats = computed(() => {
  const resumes = resumeStore.resumes
  return {
    totalResumes: resumes.length,
    averageScore: resumes.length > 0 
      ? Math.round(resumes.reduce((sum, r) => sum + (r.score || 0), 0) / resumes.length)
      : 0,
    thisMonth: resumes.filter(r => {
      const date = new Date(r.createdAt)
      const now = new Date()
      return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear()
    }).length,
    bestScore: resumes.length > 0 
      ? Math.max(...resumes.map(r => r.score || 0))
      : 0
  }
})

const filteredResumes = computed(() => {
  const resumes = resumeStore.resumes
  
  if (activeFilter.value === 'all') {
    return resumes
  }
  
  return resumes.filter(resume => {
    const score = resume.score || 0
    switch (activeFilter.value) {
      case 'excellent':
        return score >= 80
      case 'good':
        return score >= 60 && score < 80
      case 'average':
        return score >= 40 && score < 60
      case 'poor':
        return score < 40
      default:
        return true
    }
  })
})

const handleUpload = async (file) => {
  isUploading.value = true
  try {
    await resumeStore.uploadResume(file)
    uiStore.showNotification('CV téléchargé avec succès', 'success')
  } catch (error) {
    uiStore.showNotification(`Erreur: ${error.message}`, 'error')
  } finally {
    isUploading.value = false
  }
}

const handleUploadSuccess = () => {
  refreshData()
}

const selectResume = (resume) => {
  resumeStore.setCurrentResume(resume)
}

const viewAnalysis = (resume) => {
  router.push(`/result/${resume.id}`)
}

const downloadResume = async (resume) => {
  // Implementation for download
  uiStore.showNotification('Téléchargement en cours...', 'info')
}

const deleteResume = async (resume) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer "${resume.originalName}" ?`)) {
    try {
      await resumeStore.deleteResume(resume.id)
      uiStore.showNotification('CV supprimé avec succès', 'success')
    } catch (error) {
      uiStore.showNotification(`Erreur: ${error.message}`, 'error')
    }
  }
}

const refreshData = async () => {
  isLoading.value = true
  try {
    await resumeStore.fetchUserResumes()
    updateProgressChart()
  } catch (error) {
    uiStore.showNotification(`Erreur: ${error.message}`, 'error')
  } finally {
    isLoading.value = false
  }
}

const formatDate = (date) => {
  return formatters.formatDateShort(date)
}

const getScoreClass = (score) => {
  if (score >= 80) return 'score-excellent'
  if (score >= 60) return 'score-good'
  if (score >= 40) return 'score-average'
  return 'score-poor'
}

const updateProgressChart = () => {
  if (!progressChart.value) return

  const resumes = resumeStore.resumes.slice(-10) // Last 10 resumes
  const labels = resumes.map((_, index) => `CV ${index + 1}`)
  const scores = resumes.map(r => r.score || 0)

  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  const ctx = progressChart.value.getContext('2d')
  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Score du CV',
        data: scores,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: (value) => `${value}%`
          }
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  })
}

onMounted(async () => {
  await refreshData()
})
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 0.5rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover:not(:disabled) {
  border-color: #3b82f6;
  color: #3b82f6;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.stat-content p {
  color: #6b7280;
  margin: 0;
  font-size: 0.875rem;
}

/* Recent Section */
.recent-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 0.5rem 1rem;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 0.5rem;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.filter-tab:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.filter-tab--active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 1.25rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.empty-state p {
  margin-bottom: 2rem;
}

/* Resumes Grid */
.resumes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.resume-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.resume-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.resume-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.resume-info h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
  word-break: break-word;
}

.resume-info p {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.resume-score {
  font-size: 1.25rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
}

.score-excellent {
  background: #d1fae5;
  color: #10b981;
}

.score-good {
  background: #dbeafe;
  color: #3b82f6;
}

.score-average {
  background: #fed7aa;
  color: #f59e0b;
}

.score-poor {
  background: #fee2e2;
  color: #ef4444;
}

.resume-preview {
  margin-bottom: 1rem;
}

.preview-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.preview-item {
  text-align: center;
  padding: 0.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.preview-label {
  display: block;
  font-size: 0.75rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.preview-value {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.resume-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn.primary {
  background: #3b82f6;
  color: white;
}

.action-btn.primary:hover {
  background: #2563eb;
}

.action-btn.secondary {
  background: #f3f4f6;
  color: #6b7280;
}

.action-btn.secondary:hover {
  background: #e5e7eb;
}

.action-btn.danger {
  background: #fef2f2;
  color: #ef4444;
}

.action-btn.danger:hover {
  background: #fee2e2;
}

/* Chart Section */
.chart-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* Responsive */
@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .resumes-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-tabs {
    justify-content: center;
  }
  
  .resume-actions {
    justify-content: center;
  }
}
</style>
