<template>
  <div class="home">
    <div class="hero">
      <div class="container">
        <h1 class="hero-title">Optimize Your CV with AI</h1>
        <p class="hero-subtitle">
          Get instant feedback, improve your resume, and land your dream job
        </p>
        
        <div class="upload-section">
          <div class="upload-card">
            <h2>Upload Your Resume</h2>
            <p>Support PDF, DOC, and DOCX files</p>
            <input 
              type="file" 
              ref="fileInput" 
              @change="handleFileUpload"
              accept=".pdf,.doc,.docx"
              style="display: none"
            />
            <button 
              @click="$refs.fileInput.click()"
              class="btn btn-primary"
              :disabled="uploading"
            >
              {{ uploading ? 'Uploading...' : 'Choose File' }}
            </button>
            
            <div v-if="selectedFile" class="file-info">
              <p>Selected: {{ selectedFile.name }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <section class="features">
      <div class="container">
        <h2 class="section-title">Features</h2>
        <div class="features-grid">
          <div class="feature-card">
            <h3>📊 AI Analysis</h3>
            <p>Get detailed analysis of your resume with advanced AI algorithms</p>
          </div>
          <div class="feature-card">
            <h3>🎯 Skills Matching</h3>
            <p>Match your skills with job requirements and identify gaps</p>
          </div>
          <div class="feature-card">
            <h3>📈 Score Improvement</h3>
            <p>Receive actionable suggestions to improve your resume score</p>
          </div>
        </div>
      </div>
    </section>
    
    <section v-if="analysisResult" class="results">
      <div class="container">
        <h2 class="section-title">Analysis Results</h2>
        <div class="result-card">
          <div class="score-circle">
            <span class="score">{{ analysisResult.overallScore }}</span>
          </div>
          <h3>Overall Score</h3>
          
          <div class="score-breakdown">
            <div class="score-item">
              <span>Skills:</span>
              <span>{{ analysisResult.scores.skills }}/100</span>
            </div>
            <div class="score-item">
              <span>Experience:</span>
              <span>{{ analysisResult.scores.experience }}/100</span>
            </div>
            <div class="score-item">
              <span>Education:</span>
              <span>{{ analysisResult.scores.education }}/100</span>
            </div>
            <div class="score-item">
              <span>Format:</span>
              <span>{{ analysisResult.scores.format }}/100</span>
            </div>
          </div>
          
          <div class="recommendations">
            <h4>Recommendations</h4>
            <ul>
              <li v-for="rec in analysisResult.recommendations" :key="rec">
                {{ rec }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      selectedFile: null,
      uploading: false,
      analysisResult: null
    }
  },
  methods: {
    async handleFileUpload(event) {
      const file = event.target.files[0]
      if (!file) return
      
      this.selectedFile = file
      this.uploading = true
      
      try {
        // Mock upload and analysis
        await this.mockUpload(file)
        await this.mockAnalysis()
      } catch (error) {
        console.error('Upload failed:', error)
        alert('Upload failed. Please try again.')
      } finally {
        this.uploading = false
      }
    },
    
    mockUpload(file) {
      return new Promise((resolve) => {
        setTimeout(() => {
          console.log('File uploaded:', file.name)
          resolve()
        }, 2000)
      })
    },
    
    mockAnalysis() {
      return new Promise((resolve) => {
        setTimeout(() => {
          this.analysisResult = {
            overallScore: 85,
            scores: {
              skills: 88,
              experience: 82,
              education: 90,
              format: 85
            },
            recommendations: [
              'Add more quantifiable achievements to your experience section',
              'Consider including a professional summary at the top',
              'Highlight more technical skills you possess'
            ]
          }
          resolve()
        }, 3000)
      })
    }
  }
}
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.upload-section {
  margin-top: 3rem;
}

.upload-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  margin: 0 auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.upload-card h2 {
  margin-bottom: 1rem;
}

.upload-card p {
  margin-bottom: 1.5rem;
  opacity: 0.8;
}

.btn-primary {
  background: #3b82f6;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-2px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.file-info {
  margin-top: 1rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
}

.features {
  padding: 4rem 0;
  background: #f8fafc;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: #1e293b;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #3b82f6;
}

.results {
  padding: 4rem 0;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  border: 4px solid #f1f5f9;
}

.score {
  font-size: 2.5rem;
  font-weight: bold;
  color: white;
}

.score-breakdown {
  margin: 2rem 0;
}

.score-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.score-item:last-child {
  border-bottom: none;
}

.recommendations {
  margin-top: 2rem;
}

.recommendations h4 {
  margin-bottom: 1rem;
  color: #1e293b;
}

.recommendations ul {
  list-style: none;
  padding: 0;
}

.recommendations li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.recommendations li:before {
  content: "💡";
  position: absolute;
  left: 0;
}
</style>
