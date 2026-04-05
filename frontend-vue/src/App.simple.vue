<template>
  <div id="app">
    <nav class="navbar">
      <div class="container">
        <h1 class="nav-title">AI CV Optimizer</h1>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>
    
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 AI CV Optimizer. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.navbar {
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-title {
  color: #3b82f6;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #3b82f6;
  background: #f1f5f9;
}

.main-content {
  min-height: calc(100vh - 200px);
  padding: 2rem 0;
}

.footer {
  background: #f8fafc;
  padding: 2rem 0;
  text-align: center;
  color: #64748b;
}
</style>
