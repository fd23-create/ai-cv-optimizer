<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            Optimisez votre CV avec l'Intelligence Artificielle
          </h1>
          <p class="hero-subtitle">
            Analysez, améliorez et perfectionnez votre curriculum vitae avec notre technologie de pointe
          </p>
          <div class="hero-features">
            <div class="feature-item">
              <CheckCircle class="feature-icon" />
              <span>Analyse instantanée</span>
            </div>
            <div class="feature-item">
              <CheckCircle class="feature-icon" />
              <span>Suggestions personnalisées</span>
            </div>
            <div class="feature-item">
              <CheckCircle class="feature-icon" />
              <span>Optimisation par secteur</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="cv-preview">
            <FileText class="cv-icon" />
            <div class="cv-score">85%</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Upload Section -->
    <section class="upload-section">
      <div class="upload-container">
        <h2 class="section-title">Commencez l'analyse</h2>
        <p class="section-subtitle">
          Téléchargez votre CV au format PDF, DOC ou DOCX
        </p>
        
        <UploadButton
          @file-selected="handleFileSelected"
          @error="handleUploadError"
          :is-loading="isUploading"
          :loading-text="uploadProgress > 0 ? `Téléchargement... ${uploadProgress}%` : 'Analyse en cours...'"
        />
        
        <div v-if="currentFile" class="file-info">
          <div class="file-details">
            <FileText class="file-icon" />
            <div class="file-meta">
              <span class="file-name">{{ currentFile.name }}</span>
              <span class="file-size">{{ formatFileSize(currentFile.size) }}</span>
            </div>
          </div>
          
          <ProgressBar
            v-if="isAnalyzing || uploadProgress > 0"
            :value="uploadProgress || analysisProgress"
            :label="isAnalyzing ? 'Analyse du CV' : 'Téléchargement'"
            :status="isAnalyzing ? 'loading' : 'success'"
          />
        </div>
        
        <div v-if="analysisResult" class="quick-results">
          <div class="result-header">
            <h3>Analyse rapide</h3>
            <button @click="goToResult" class="view-details-btn">
              Voir les détails
              <ArrowRight />
            </button>
          </div>
          
          <div class="result-cards">
            <ScoreCard
              :score="analysisResult.overallScore"
              title="Score global"
              :subtitle="getScoreDescription(analysisResult.overallScore)"
              :compact="true"
            />
            
            <div class="mini-stats">
              <div class="stat-item">
                <span class="stat-label">Compétences</span>
                <span class="stat-value">{{ analysisResult.skillsCount }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Expériences</span>
                <span class="stat-value">{{ analysisResult.experienceCount }}</span>
              </div>
              <div class="stat-item">
                <span class="stat-label">Formation</span>
                <span class="stat-value">{{ analysisResult.educationCount }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="features-container">
        <h2 class="section-title">Pourquoi choisir notre solution ?</h2>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <Brain class="feature-card-icon" />
            </div>
            <h3>Analyse IA avancée</h3>
            <p>Notre algorithme analyse en profondeur votre CV pour identifier les points forts et les axes d'amélioration.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <Target class="feature-card-icon" />
            </div>
            <h3>Optimisation sectorielle</h3>
            <p>Adaptez votre CV aux exigences spécifiques de votre secteur d'activité visé.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <TrendingUp class="feature-card-icon" />
            </div>
            <h3>Suivi de progression</h3>
            <p>Visualisez l'amélioration de votre CV au fil du temps avec des analyses comparatives.</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon-wrapper">
              <Shield class="feature-card-icon" />
            </div>
            <h3>Confidentialité garantie</h3>
            <p>Vos données sont sécurisées et ne sont jamais partagées avec des tiers.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="cta-container">
        <h2>Prêt à optimiser votre CV ?</h2>
        <p>Rejoignez des milliers de professionnels qui ont amélioré leur carrière avec notre aide.</p>
        <div class="cta-buttons">
          <button @click="scrollToUpload" class="cta-btn primary">
            Commencer maintenant
          </button>
          <router-link to="/dashboard" class="cta-btn secondary">
            Voir le tableau de bord
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@clerk/clerk-vue'
import { useResumeStore } from '@/store/resumeStore.js'
import { useUIStore } from '@/store/uiStore.js'
import { formatters } from '@/utils/formatters.js'
import UploadButton from '@/components/UploadButton.vue'
import ProgressBar from '@/components/ProgressBar.vue'
import ScoreCard from '@/components/ScoreCard.vue'
import {
  CheckCircle,
  FileText,
  ArrowRight,
  Brain,
  Target,
  TrendingUp,
  Shield
} from 'lucide-vue-next'

const router = useRouter()
const { isSignedIn } = useAuth()
const resumeStore = useResumeStore()
const uiStore = useUIStore()

const currentFile = ref(null)
const isUploading = ref(false)
const isAnalyzing = ref(false)
const uploadProgress = ref(0)
const analysisProgress = ref(0)
const analysisResult = ref(null)

const handleFileSelected = async (file) => {
  if (!isSignedIn.value) {
    uiStore.showNotification('Veuillez vous connecter pour analyser votre CV', 'warning')
    return
  }

  currentFile.value = file
  isUploading.value = true
  uploadProgress.value = 0

  try {
    // Simulate upload progress
    const uploadInterval = setInterval(() => {
      uploadProgress.value += 10
      if (uploadProgress.value >= 100) {
        clearInterval(uploadInterval)
        startAnalysis()
      }
    }, 200)

    const result = await resumeStore.uploadResume(file)
    uploadProgress.value = 100
    
  } catch (error) {
    handleUploadError(error.message)
  } finally {
    isUploading.value = false
  }
}

const startAnalysis = async () => {
  isAnalyzing.value = true
  analysisProgress.value = 0

  try {
    // Simulate analysis progress
    const analysisInterval = setInterval(() => {
      analysisProgress.value += 5
      if (analysisProgress.value >= 100) {
        clearInterval(analysisInterval)
        completeAnalysis()
      }
    }, 300)

    const result = await resumeStore.analyzeResume(resumeStore.currentResume.id)
    
  } catch (error) {
    handleUploadError(error.message)
  } finally {
    isAnalyzing.value = false
  }
}

const completeAnalysis = () => {
  // Mock analysis result for demo
  analysisResult.value = {
    overallScore: 85,
    skillsCount: 12,
    experienceCount: 3,
    educationCount: 2,
    recommendations: [
      'Ajoutez plus de mots-clés techniques',
      'Quantifiez vos réalisations',
      'Améliorez la lisibilité de la mise en page'
    ]
  }
  
  uiStore.showNotification('Analyse terminée avec succès !', 'success')
}

const handleUploadError = (error) => {
  uiStore.showNotification(`Erreur: ${error}`, 'error')
  currentFile.value = null
  uploadProgress.value = 0
  analysisProgress.value = 0
}

const goToResult = () => {
  if (resumeStore.currentResume) {
    router.push(`/result/${resumeStore.currentResume.id}`)
  }
}

const scrollToUpload = () => {
  const uploadSection = document.querySelector('.upload-section')
  uploadSection?.scrollIntoView({ behavior: 'smooth' })
}

const formatFileSize = (bytes) => {
  return formatters.formatFileSize(bytes)
}

const getScoreDescription = (score) => {
  if (score >= 80) return 'Excellent'
  if (score >= 60) return 'Bon'
  if (score >= 40) return 'Moyen'
  return 'À améliorer'
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 2rem;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.125rem;
}

.feature-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.cv-preview {
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  padding: 3rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cv-icon {
  width: 120px;
  height: 120px;
  color: rgba(255, 255, 255, 0.8);
}

.cv-score {
  position: absolute;
  top: -10px;
  right: -10px;
  background: #10b981;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid white;
}

/* Upload Section */
.upload-section {
  padding: 4rem 2rem;
  background: #f8fafc;
}

.upload-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.section-title {
  font-size: 2rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.section-subtitle {
  color: #6b7280;
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

.file-info {
  margin-top: 2rem;
  text-align: left;
}

.file-details {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  margin-bottom: 1rem;
}

.file-icon {
  width: 24px;
  height: 24px;
  color: #3b82f6;
}

.file-meta {
  display: flex;
  flex-direction: column;
}

.file-name {
  font-weight: 500;
  color: #1f2937;
}

.file-size {
  font-size: 0.875rem;
  color: #6b7280;
}

.quick-results {
  margin-top: 2rem;
  text-align: left;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.result-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.view-details-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.view-details-btn:hover {
  background: #2563eb;
}

.result-cards {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
}

.mini-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.stat-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

/* Features Section */
.features-section {
  padding: 4rem 2rem;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.feature-icon-wrapper {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.feature-card-icon {
  width: 32px;
  height: 32px;
  color: white;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #6b7280;
  line-height: 1.6;
}

/* CTA Section */
.cta-section {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.cta-container {
  max-width: 600px;
  margin: 0 auto;
}

.cta-section h2 {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.cta-section p {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-btn {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.cta-btn.primary {
  background: #3b82f6;
  color: white;
}

.cta-btn.primary:hover {
  background: #2563eb;
}

.cta-btn.secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.cta-btn.secondary:hover {
  background: white;
  color: #1f2937;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .result-cards {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .cta-btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>
