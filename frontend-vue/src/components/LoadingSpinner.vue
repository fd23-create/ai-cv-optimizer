<template>
  <div class="loading-spinner" :class="[`loading-spinner--${size}`, { 'loading-spinner--overlay': overlay }]">
    <div class="spinner-container">
      <div class="spinner" :class="{ 'spinner--pulse': pulse }">
        <div v-if="type === 'dots'" class="dots-spinner">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
        
        <div v-else-if="type === 'ring'" class="ring-spinner">
          <div class="ring"></div>
        </div>
        
        <div v-else-if="type === 'wave'" class="wave-spinner">
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
          <div class="wave-bar"></div>
        </div>
        
        <div v-else class="default-spinner">
          <div class="spinner-circle"></div>
        </div>
      </div>
      
      <div v-if="text" class="spinner-text">
        {{ text }}
      </div>
      
      <div v-if="showProgress && progress !== null" class="spinner-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: `${progress}%` }"></div>
        </div>
        <span class="progress-text">{{ Math.round(progress) }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  type: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'dots', 'ring', 'wave'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  overlay: {
    type: Boolean,
    default: false
  },
  pulse: {
    type: Boolean,
    default: false
  },
  showProgress: {
    type: Boolean,
    default: false
  },
  progress: {
    type: Number,
    default: null,
    validator: (value) => value === null || (value >= 0 && value <= 100)
  }
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-spinner--overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  z-index: 9999;
}

.loading-spinner--small {
  padding: 1rem;
}

.loading-spinner--medium {
  padding: 2rem;
}

.loading-spinner--large {
  padding: 3rem;
}

.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner--pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Default Spinner */
.default-spinner {
  width: 40px;
  height: 40px;
}

.spinner-circle {
  width: 100%;
  height: 100%;
  border: 3px solid #e5e7eb;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Dots Spinner */
.dots-spinner {
  display: flex;
  gap: 0.25rem;
}

.dot {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  animation: dots-bounce 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) {
  animation-delay: -0.32s;
}

.dot:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes dots-bounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Ring Spinner */
.ring-spinner {
  width: 40px;
  height: 40px;
  position: relative;
}

.ring {
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top: 3px solid #3b82f6;
  border-right: 3px solid #3b82f6;
  border-radius: 50%;
  animation: ring-spin 1s linear infinite;
}

@keyframes ring-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Wave Spinner */
.wave-spinner {
  display: flex;
  gap: 0.25rem;
  align-items: flex-end;
  height: 40px;
}

.wave-bar {
  width: 4px;
  height: 20px;
  background: #3b82f6;
  border-radius: 2px;
  animation: wave-stretch 1.2s ease-in-out infinite;
}

.wave-bar:nth-child(1) {
  animation-delay: -1.1s;
}

.wave-bar:nth-child(2) {
  animation-delay: -1.0s;
}

.wave-bar:nth-child(3) {
  animation-delay: -0.9s;
}

.wave-bar:nth-child(4) {
  animation-delay: -0.8s;
}

.wave-bar:nth-child(5) {
  animation-delay: -0.7s;
}

@keyframes wave-stretch {
  0%, 40%, 100% {
    transform: scaleY(0.4);
  }
  20% {
    transform: scaleY(1);
  }
}

/* Text and Progress */
.spinner-text {
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
  font-weight: 500;
}

.spinner-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  width: 200px;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

/* Size variations */
.loading-spinner--small .default-spinner,
.loading-spinner--small .ring-spinner {
  width: 24px;
  height: 24px;
}

.loading-spinner--small .spinner-circle {
  border-width: 2px;
  border-top-width: 2px;
}

.loading-spinner--small .ring {
  border-width: 2px;
  border-top-width: 2px;
  border-right-width: 2px;
}

.loading-spinner--small .wave-spinner {
  height: 24px;
}

.loading-spinner--small .wave-bar {
  height: 12px;
  width: 3px;
}

.loading-spinner--large .default-spinner,
.loading-spinner--large .ring-spinner {
  width: 56px;
  height: 56px;
}

.loading-spinner--large .spinner-circle {
  border-width: 4px;
  border-top-width: 4px;
}

.loading-spinner--large .ring {
  border-width: 4px;
  border-top-width: 4px;
  border-right-width: 4px;
}

.loading-spinner--large .wave-spinner {
  height: 56px;
}

.loading-spinner--large .wave-bar {
  height: 28px;
  width: 6px;
}

.loading-spinner--large .dot {
  width: 12px;
  height: 12px;
}
</style>
