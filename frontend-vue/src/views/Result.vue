<template>
  <div class="result">
    <div v-if="isLoading" class="loading-container">
      <LoadingSpinner size="large" text="Chargement de l'analyse..." />
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-content">
        <AlertCircle class="error-icon" />
        <h2>Une erreur est survenue</h2>
        <p>{{ error }}</p>
        <button @click="goBack" class="back-btn">Retour</button>
      </div>
    </div>

    <div v-else-if="analysisResult" class="result-content">
      <!-- Header -->
      <div class="result-header">
        <div class="header-info">
          <h1>Résultats de l'analyse</h1>
          <div class="resume-meta">
            <span class="resume-name">{{ resumeInfo?.originalName }}</span>
            <span class="analysis-date">{{ formatDate(analysisResult.createdAt) }}</span>
          </div>
        </div>
        <div class="header-actions">
          <button @click="exportPDF" class="action-btn primary">
            <Download />
            Exporter PDF
          </button>
          <button @click="shareResults" class="action-btn secondary">
            <Share2 />
            Partager
          </button>
        </div>
      </div>

      <!-- Overall Score -->
      <div class="score-section">
        <ScoreCard
          :score="analysisResult.overallScore"
          title="Score global"
          :subtitle="getScoreDescription(analysisResult.overallScore)"
          :description="getScoreFeedback(analysisResult.overallScore)"
          :recommendations="analysisResult.recommendations?.slice(0, 3) || []"
          :details="scoreDetails"
          :show-details="true"
        />
      </div>

      <!-- Detailed Analysis -->
      <div class="analysis-grid">
        <!-- Skills Analysis -->
        <div class="analysis-card">
          <h3>
            <Brain />
            Analyse des compétences
          </h3>
          <div class="skills-content">
            <SkillsChart
              :skills="analysisResult.skills || []"
              :show-legend="true"
              :max-skills="8"
            />
            <div v-if="analysisResult.missingSkills?.length > 0" class="missing-skills">
              <h4>Compétences suggérées</h4>
              <div class="skills-tags">
                <span
                  v-for="skill in analysisResult.missingSkills"
                  :key="skill"
                  class="skill-tag missing"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Experience Analysis -->
        <div class="analysis-card">
          <h3>
            <Briefcase />
            Analyse de l'expérience
          </h3>
          <div class="experience-content">
            <div class="experience-stats">
              <div class="stat-item">
                <span class="stat-label">Total d'années</span>
                <span class="stat-value">{{ analysisResult.totalExperience || 0 }} ans</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Nombre de postes</span>
                <span class="stat-value">{{ analysisResult.experienceCount || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Progression de carrière</span>
                <span class="stat-value" :class="getProgressionClass(analysisResult.careerProgression)">
                  {{ getProgressionText(analysisResult.careerProgression) }}
                </span>
              </div>
            </div>
            
            <div v-if="analysisResult.experienceFeedback" class="feedback-section">
              <h4>Conseils</h4>
              <ul class="feedback-list">
                <li v-for="feedback in analysisResult.experienceFeedback" :key="feedback">
                  {{ feedback }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Education Analysis -->
        <div class="analysis-card">
          <h3>
            <GraduationCap />
            Analyse de la formation
          </h3>
          <div class="education-content">
            <div class="education-stats">
              <div class="stat-item">
                <span class="stat-label">Niveau d'études</span>
                <span class="stat-value">{{ analysisResult.educationLevel || 'Non spécifié' }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Nombre de diplômes</span>
                <span class="stat-value">{{ analysisResult.educationCount || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Pertinence</span>
                <span class="stat-value" :class="getRelevanceClass(analysisResult.educationRelevance)">
                  {{ getRelevanceText(analysisResult.educationRelevance) }}
                </span>
              </div>
            </div>
            
            <div v-if="analysisResult.educationFeedback" class="feedback-section">
              <h4>Recommandations</h4>
              <ul class="feedback-list">
                <li v-for="feedback in analysisResult.educationFeedback" :key="feedback">
                  {{ feedback }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Format & Structure -->
        <div class="analysis-card">
          <h3>
            <Layout />
            Format et structure
          </h3>
          <div class="format-content">
            <div class="format-checks">
              <div
                v-for="check in formatChecks"
                :key="check.name"
                class="check-item"
                :class="{ 'check-item--fail': !check.passed }"
              >
                <component :is="check.passed ? Check : X" class="check-icon" />
                <span class="check-label">{{ check.label }}</span>
              </div>
            </div>
            
            <div class="format-score">
              <ProgressBar
                :value="analysisResult.formatScore || 0"
                label="Score de formatage"
                :show-status="true"
                :status="getFormatStatus(analysisResult.formatScore)"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Feedback -->
      <div class="feedback-section">
        <h2>Recommandations détaillées</h2>
        <div class="feedback-categories">
          <div
            v-for="category in feedbackCategories"
            :key="category.name"
            class="feedback-category"
          >
            <h3>
              <component :is="category.icon" />
              {{ category.title }}
            </h3>
            <ul class="feedback-list">
              <li v-for="item in category.items" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="action-section">
        <button @click="regenerateAnalysis" class="action-btn primary large">
          <RefreshCw />
          Relancer l'analyse
        </button>
        <button @click="goToDashboard" class="action-btn secondary large">
          <LayoutDashboard />
          Tableau de bord
        </button>
        <button @click="uploadNewResume" class="action-btn outline large">
          <Upload />
          Nouveau CV
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useResumeStore } from '@/store/resumeStore.js'
import { useUIStore } from '@/store/uiStore.js'
import { formatters } from '@/utils/formatters.js'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ScoreCard from '@/components/ScoreCard.vue'
import SkillsChart from '@/components/SkillsChart.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import {
  AlertCircle,
  Download,
  Share2,
  Brain,
  Briefcase,
  GraduationCap,
  Layout,
  Check,
  X,
  RefreshCw,
  LayoutDashboard,
  Upload,
  Target,
  FileText,
  Eye
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const resumeStore = useResumeStore()
const uiStore = useUIStore()

const isLoading = ref(true)
const error = ref(null)

const resumeInfo = computed(() => resumeStore.currentResume)
const analysisResult = computed(() => resumeStore.currentAnalysis)

const scoreDetails = computed(() => {
  if (!analysisResult.value) return {}
  
  return {
    'Compétences techniques': analysisResult.value.skillsScore || 0,
    'Expérience professionnelle': analysisResult.value.experienceScore || 0,
    'Formation': analysisResult.value.educationScore || 0,
    'Format et présentation': analysisResult.value.formatScore || 0
  }
})

const formatChecks = computed(() => {
  if (!analysisResult.value?.formatChecks) return []
  
  return [
    {
      name: 'length',
      label: 'Longueur appropriée (1-2 pages)',
      passed: analysisResult.value.formatChecks.length || false
    },
    {
      name: 'contact',
      label: 'Informations de contact complètes',
      passed: analysisResult.value.formatChecks.contact || false
    },
    {
      name: 'structure',
      label: 'Structure logique',
      passed: analysisResult.value.formatChecks.structure || false
    },
    {
      name: 'grammar',
      label: 'Absence de fautes d\'orthographe',
      passed: analysisResult.value.formatChecks.grammar || false
    },
    {
      name: 'keywords',
      label: 'Mots-clés pertinents',
      passed: analysisResult.value.formatChecks.keywords || false
    }
  ]
})

const feedbackCategories = computed(() => {
  if (!analysisResult.value?.detailedFeedback) return []
  
  const feedback = analysisResult.value.detailedFeedback
  
  return [
    {
      name: 'improvements',
      title: 'Améliorations suggérées',
      icon: Target,
      items: feedback.improvements || []
    },
    {
      name: 'strengths',
      title: 'Points forts',
      icon: Check,
      items: feedback.strengths || []
    },
    {
      name: 'actionable',
      title: 'Actions concrètes',
      icon: FileText,
      items: feedback.actionable || []
    }
  ].filter(category => category.items.length > 0)
})

const loadAnalysis = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const resumeId = route.params.id
    await resumeStore.getResumeById(resumeId)
    
    if (resumeStore.currentResume?.analysisId) {
      await resumeStore.getAnalysisResult(resumeStore.currentResume.analysisId)
    } else {
      // If no analysis exists, create one
      await resumeStore.analyzeResume(resumeId)
    }
  } catch (err) {
    error.value = err.message || 'Impossible de charger l\'analyse'
    uiStore.showNotification(error.value, 'error')
  } finally {
    isLoading.value = false
  }
}

const getScoreDescription = (score) => {
  if (score >= 90) return 'Excellent - Votre CV est très performant'
  if (score >= 80) return 'Très bon - Votre CV est bien structuré'
  if (score >= 70) return 'Bon - Votre CV a des points forts'
  if (score >= 60) return 'Moyen - Des améliorations sont possibles'
  if (score >= 50) return 'Correct - Des améliorations sont nécessaires'
  return 'Faible - Une révision importante est recommandée'
}

const getScoreFeedback = (score) => {
  if (score >= 80) {
    return 'Félicitations ! Votre CV est bien structuré et présente efficacement vos compétences et expériences. Quelques ajustements mineurs pourraient encore l\'améliorer.'
  } else if (score >= 60) {
    return 'Votre CV est dans la bonne direction. En appliquant les recommandations ci-dessous, vous pourriez significativement améliorer son impact.'
  } else {
    return 'Votre CV nécessite des améliorations importantes pour être plus efficace. Suivez attentivement les recommandations pour optimiser votre présentation.'
  }
}

const getProgressionClass = (progression) => {
  switch (progression) {
    case 'strong': return 'positive'
    case 'moderate': return 'neutral'
    case 'weak': return 'negative'
    default: return 'neutral'
  }
}

const getProgressionText = (progression) => {
  switch (progression) {
    case 'strong': return 'Forte progression'
    case 'moderate': return 'Progression modérée'
    case 'weak': return 'Progression limitée'
    default: return 'Non évaluée'
  }
}

const getRelevanceClass = (relevance) => {
  switch (relevance) {
    case 'high': return 'positive'
    case 'medium': return 'neutral'
    case 'low': return 'negative'
    default: return 'neutral'
  }
}

const getRelevanceText = (relevance) => {
  switch (relevance) {
    case 'high': return 'Très pertinente'
    case 'medium': return 'Moyennement pertinente'
    case 'low': return 'Peu pertinente'
    default: return 'Non évaluée'
  }
}

const getFormatStatus = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'error'
}

const exportPDF = () => {
  uiStore.showNotification('Export PDF en cours...', 'info')
  // Implementation for PDF export
}

const shareResults = () => {
  uiStore.showNotification('Lien de partage copié !', 'success')
  // Implementation for sharing
}

const regenerateAnalysis = async () => {
  if (!resumeInfo.value) return
  
  try {
    await resumeStore.analyzeResume(resumeInfo.value.id)
    uiStore.showNotification('Analyse relancée avec succès', 'success')
  } catch (err) {
    uiStore.showNotification(`Erreur: ${err.message}`, 'error')
  }
}

const goBack = () => {
  router.go(-1)
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const uploadNewResume = () => {
  router.push('/')
}

const formatDate = (date) => {
  return formatters.formatDate(date)
}

onMounted(() => {
  loadAnalysis()
})
</script>

<style scoped>
.result {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Loading and Error States */
.loading-container,
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.error-content {
  text-align: center;
  color: #6b7280;
}

.error-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 1rem;
  color: #ef4444;
}

.error-content h2 {
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.back-btn {
  padding: 0.75rem 1.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

/* Result Header */
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-info h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.resume-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.resume-name {
  font-weight: 500;
  color: #1f2937;
}

.analysis-date {
  color: #6b7280;
  font-size: 0.875rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
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

.action-btn.outline {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.action-btn.outline:hover {
  background: #3b82f6;
  color: white;
}

.action-btn.large {
  padding: 1rem 2rem;
  font-size: 1rem;
}

/* Score Section */
.score-section {
  margin-bottom: 2rem;
}

/* Analysis Grid */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.analysis-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.analysis-card h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.analysis-card h3 svg {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

/* Skills Content */
.skills-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.missing-skills h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.skills-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.skill-tag.missing {
  background: #fef3c7;
  color: #92400e;
}

/* Experience Content */
.experience-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.experience-stats,
.education-stats {
  display: grid;
  gap: 1rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.stat-value {
  font-weight: 600;
  color: #1f2937;
}

.stat-value.positive {
  color: #10b981;
}

.stat-value.negative {
  color: #ef4444;
}

.stat-value.neutral {
  color: #f59e0b;
}

/* Feedback Section */
.feedback-section {
  margin-bottom: 1.5rem;
}

.feedback-section h4 {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.feedback-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feedback-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  padding: 0.5rem 0;
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
}

.feedback-list li::before {
  content: "•";
  color: #3b82f6;
  font-weight: bold;
  margin-top: 0.125rem;
}

/* Format Content */
.format-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.format-checks {
  display: grid;
  gap: 0.75rem;
}

.check-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border-left: 4px solid #10b981;
}

.check-item--fail {
  border-left-color: #ef4444;
}

.check-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.check-item .check-icon {
  color: #10b981;
}

.check-item--fail .check-icon {
  color: #ef4444;
}

.check-label {
  color: #4b5563;
  font-size: 0.875rem;
}

/* Detailed Feedback */
.feedback-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.feedback-categories {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.feedback-category {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.feedback-category h3 {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.feedback-category h3 svg {
  width: 20px;
  height: 20px;
  color: #3b82f6;
}

/* Action Section */
.action-section {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

/* Responsive */
@media (max-width: 768px) {
  .result {
    padding: 1rem;
  }
  
  .result-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: stretch;
  }
  
  .action-btn {
    justify-content: center;
  }
  
  .analysis-grid {
    grid-template-columns: 1fr;
  }
  
  .feedback-categories {
    grid-template-columns: 1fr;
  }
  
  .action-section {
    flex-direction: column;
  }
  
  .action-btn.large {
    width: 100%;
  }
}
</style>
