import { createApp } from 'vue'

const app = createApp({
  template: `
    <div>
      <h1>AI CV Optimizer</h1>
      <p>Frontend is working! 🎉</p>
      <p>Backend API: <a href="http://localhost:5000/health" target="_blank">http://localhost:5000/health</a></p>
    </div>
  `
})

app.mount('#app')
