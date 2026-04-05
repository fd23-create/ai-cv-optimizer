<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <p>Manage your resumes and track your progress</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <h3>Total Resumes</h3>
        <div class="stat-number">5</div>
      </div>
      <div class="stat-card">
        <h3>Average Score</h3>
        <div class="stat-number">82%</div>
      </div>
      <div class="stat-card">
        <h3>Analyses Completed</h3>
        <div class="stat-number">12</div>
      </div>
    </div>
    
    <div class="recent-resumes">
      <h2>Recent Resumes</h2>
      <div class="resume-list">
        <div class="resume-item">
          <div class="resume-info">
            <h4>Software Engineer Resume</h4>
            <p>Last updated: 2 days ago</p>
          </div>
          <div class="resume-score">85</div>
        </div>
        <div class="resume-item">
          <div class="resume-info">
            <h4>Product Manager Resume</h4>
            <p>Last updated: 1 week ago</p>
          </div>
          <div class="resume-score">78</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard'
}
</script>

<style scoped>
.dashboard {
  padding: 2rem 0;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  color: #64748b;
  margin-bottom: 1rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #3b82f6;
}

.recent-resumes h2 {
  margin-bottom: 2rem;
  color: #1e293b;
}

.resume-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.resume-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.resume-item:last-child {
  border-bottom: none;
}

.resume-info h4 {
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.resume-info p {
  color: #64748b;
  font-size: 0.9rem;
}

.resume-score {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3b82f6;
}
</style>
