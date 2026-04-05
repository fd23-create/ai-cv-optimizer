<template>
  <div id="app">
    <header class="app-header">
      <nav class="navbar">
        <div class="nav-brand">
          <router-link to="/" class="brand-link">
            <h1>AI CV Optimizer</h1>
          </router-link>
        </div>
        <div class="nav-links">
          <router-link to="/" class="nav-link">Accueil</router-link>
          <router-link to="/dashboard" class="nav-link">Tableau de bord</router-link>
          <div v-if="isSignedIn" class="user-menu">
            <SignedIn>
              <UserButton />
            </SignedIn>
          </div>
          <div v-else class="auth-buttons">
            <SignedOut>
              <SignInButton mode="modal" />
              <SignUpButton mode="modal" />
            </SignedOut>
          </div>
        </div>
      </nav>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>&copy; 2024 AI CV Optimizer. Tous droits réservés.</p>
    </footer>
  </div>
</template>

<script setup>
import { UserButton, SignedIn, SignedOut, SignInButton, SignUpButton } from '@clerk/clerk-vue'
import { useUser } from '@clerk/clerk-vue'
import { computed } from 'vue'

const { isSignedIn } = useUser()
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-link {
  text-decoration: none;
  color: white;
}

.brand-link h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s ease;
}

.nav-link:hover {
  opacity: 0.8;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
}

.main-content {
  min-height: calc(100vh - 120px);
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.app-footer {
  background: #f8f9fa;
  text-align: center;
  padding: 1rem;
  color: #6c757d;
  border-top: 1px solid #dee2e6;
}
</style>
