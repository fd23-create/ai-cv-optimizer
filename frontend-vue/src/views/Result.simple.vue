<template>
  <div class="result">
    <div class="result-header">
      <h1>Analysis Results</h1>
      <p>Detailed analysis of your resume</p>
    </div>
    
    <div class="score-overview">
      <div class="main-score">
        <div class="score-circle">
          <span class="score">85</span>
        </div>
        <h2>Overall Score</h2>
        <p>Your resume is in good shape!</p>
      </div>
      
      <div class="score-details">
        <div class="score-item">
          <span class="label">Skills</span>
          <span class="value">88/100</span>
        </div>
        <div class="score-item">
          <span class="label">Experience</span>
          <span class="value">82/100</span>
        </div>
        <div class="score-item">
          <span class="label">Education</span>
          <span class="value">90/100</span>
        </div>
        <div class="score-item">
          <span class="label">Format</span>
          <span class="value">85/100</span>
        </div>
      </div>
    </div>
    
    <div class="recommendations-section">
      <h2>Recommendations</h2>
      <div class="recommendations">
        <div class="recommendation-card">
          <h3>🎯 Skills</h3>
          <ul>
            <li>Add more technical skills to showcase your expertise</li>
            <li>Include proficiency levels for each skill</li>
          </ul>
        </div>
        
        <div class="recommendation-card">
          <h3>💼 Experience</h3>
          <ul>
            <li>Add quantifiable achievements with metrics</li>
            <li>Use more action verbs in descriptions</li>
          </ul>
        </div>
        
        <div class="recommendation-card">
          <h3>📄 Format</h3>
          <ul>
            <li>Ensure consistent formatting throughout</li>
            <li>Add more white space for readability</li>
          </ul>
        </div>
      </div>
    </div>
    
    <div class="actions">
      <button class="btn btn-primary">Download Report</button>
      <button class="btn btn-secondary">Share Results</button>
      <router-link to="/" class="btn btn-outline">Analyze Another Resume</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Result'
}
</script>

<style scoped>
.result {
  padding: 2rem 0;
}

.result-header {
  text-align: center;
  margin-bottom: 3rem;
}

.result-header h1 {
  font-size: 2.5rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.score-overview {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  margin-bottom: 3rem;
  align-items: center;
}

.main-score {
  text-align: center;
}

.score-circle {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
  border: 4px solid #f1f5f9;
}

.score {
  font-size: 3rem;
  font-weight: bold;
  color: white;
}

.main-score h2 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.score-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.score-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.score-item .label {
  font-weight: 600;
  color: #64748b;
}

.score-item .value {
  font-weight: bold;
  color: #3b82f6;
}

.recommendations-section {
  margin-bottom: 3rem;
}

.recommendations-section h2 {
  text-align: center;
  font-size: 2rem;
  color: #1e293b;
  margin-bottom: 2rem;
}

.recommendations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.recommendation-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.recommendation-card h3 {
  margin-bottom: 1rem;
  color: #1e293b;
}

.recommendation-card ul {
  list-style: none;
  padding: 0;
}

.recommendation-card li {
  padding: 0.5rem 0;
  padding-left: 1.5rem;
  position: relative;
}

.recommendation-card li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #3b82f6;
}

.actions {
  text-align: center;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  text-decoration: none;
  display: inline-block;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #64748b;
  color: white;
}

.btn-secondary:hover {
  background: #475569;
}

.btn-outline {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.btn-outline:hover {
  background: #3b82f6;
  color: white;
}

@media (max-width: 768px) {
  .score-overview {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>
