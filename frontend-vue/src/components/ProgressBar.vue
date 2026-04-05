<template>
  <div class="progress-bar">
    <div class="progress-header">
      <span class="progress-label">{{ label }}</span>
      <span class="progress-percentage">{{ percentage }}%</span>
    </div>
    
    <div class="progress-track">
      <div
        class="progress-fill"
        :style="{ width: `${percentage}%` }"
        :class="{
          'progress-fill--success': percentage === 100,
          'progress-fill--warning': percentage >= 70 && percentage < 100,
          'progress-fill--danger': percentage < 70
        }"
      >
        <div v-if="showAnimation" class="progress-shine"></div>
      </div>
    </div>
    
    <div v-if="showStatus" class="progress-status">
      <component :is="statusIcon" class="status-icon" />
      <span class="status-text">{{ statusText }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { CheckCircle, AlertCircle, Clock, Loader } from 'lucide-vue-next'

const props = defineProps({
  value: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  label: {
    type: String,
    default: 'Progression'
  },
  showStatus: {
    type: Boolean,
    default: true
  },
  showAnimation: {
    type: Boolean,
    default: true
  },
  status: {
    type: String,
    default: 'loading', // loading, success, warning, error
    validator: (value) => ['loading', 'success', 'warning', 'error'].includes(value)
  }
})

const percentage = computed(() => Math.round(props.value))

const statusIcon = computed(() => {
  switch (props.status) {
    case 'success':
      return CheckCircle
    case 'warning':
      return AlertCircle
    case 'error':
      return AlertCircle
    case 'loading':
    default:
      return Loader
  }
})

const statusText = computed(() => {
  switch (props.status) {
    case 'success':
      return 'Terminé'
    case 'warning':
      return 'Attention'
    case 'error':
      return 'Erreur'
    case 'loading':
    default:
      return 'En cours...'
  }
})
</script>

<style scoped>
.progress-bar {
  width: 100%;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-weight: 500;
  color: #374151;
}

.progress-percentage {
  font-weight: 600;
  color: #6b7280;
}

.progress-track {
  width: 100%;
  height: 0.75rem;
  background: #f3f4f6;
  border-radius: 0.375rem;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  border-radius: 0.375rem;
  transition: width 0.3s ease;
  position: relative;
  overflow: hidden;
}

.progress-fill--success {
  background: linear-gradient(90deg, #10b981, #059669);
}

.progress-fill--warning {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.progress-fill--danger {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.progress-fill:not(.progress-fill--success):not(.progress-fill--warning):not(.progress-fill--danger) {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.progress-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shine 2s infinite;
}

@keyframes shine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.progress-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.status-icon {
  width: 16px;
  height: 16px;
}

.status-text {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Animation for loading state */
.progress-fill:not(.progress-fill--success):not(.progress-fill--warning):not(.progress-fill--danger) .status-icon {
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
</style>
