<template>
  <div class="score-card" :class="[`score-card--${scoreLevel}`, { 'score-card--compact': compact }]">
    <div class="score-header">
      <div class="score-icon" :class="`score-icon--${scoreLevel}`">
        <component :is="scoreIcon" />
      </div>
      <div class="score-info">
        <h3 class="score-title">{{ title }}</h3>
        <p v-if="subtitle" class="score-subtitle">{{ subtitle }}</p>
      </div>
    </div>
    
    <div class="score-content">
      <div class="score-value">
        <span class="score-number">{{ formattedScore }}</span>
        <span class="score-max">/100</span>
      </div>
      
      <div class="score-progress">
        <div class="score-track">
          <div
            class="score-fill"
            :style="{ width: `${score}%` }"
            :class="`score-fill--${scoreLevel}`"
          ></div>
        </div>
      </div>
      
      <div v-if="description" class="score-description">
        {{ description }}
      </div>
      
      <div v-if="recommendations.length > 0" class="score-recommendations">
        <h4 class="recommendations-title">Recommandations</h4>
        <ul class="recommendations-list">
          <li v-for="recommendation in recommendations" :key="recommendation" class="recommendation-item">
            <ChevronRight class="recommendation-icon" />
            {{ recommendation }}
          </li>
        </ul>
      </div>
    </div>
    
    <div v-if="showDetails" class="score-footer">
      <button @click="toggleDetails" class="details-btn">
        <ChevronDown :class="{ 'rotate-180': showFullDetails }" />
        {{ showFullDetails ? 'Masquer' : 'Voir' }} les détails
      </button>
    </div>
    
    <div v-if="showFullDetails && details" class="score-details">
      <div class="details-content">
        <slot name="details">
          <div v-for="(value, key) in details" :key="key" class="detail-item">
            <span class="detail-label">{{ formatLabel(key) }}</span>
            <span class="detail-value">{{ formatValue(value) }}</span>
          </div>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  ChevronRight, 
  ChevronDown 
} from 'lucide-vue-next'

const props = defineProps({
  score: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100
  },
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  },
  recommendations: {
    type: Array,
    default: () => []
  },
  details: {
    type: Object,
    default: null
  },
  compact: {
    type: Boolean,
    default: false
  },
  showDetails: {
    type: Boolean,
    default: false
  }
})

const showFullDetails = ref(false)

const formattedScore = computed(() => Math.round(props.score))

const scoreLevel = computed(() => {
  if (props.score >= 80) return 'excellent'
  if (props.score >= 60) return 'good'
  if (props.score >= 40) return 'average'
  return 'poor'
})

const scoreIcon = computed(() => {
  switch (scoreLevel.value) {
    case 'excellent':
      return TrendingUp
    case 'good':
      return TrendingUp
    case 'average':
      return Minus
    case 'poor':
      return TrendingDown
    default:
      return Minus
  }
})

const toggleDetails = () => {
  showFullDetails.value = !showFullDetails.value
}

const formatLabel = (key) => {
  return key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, (str) => str.toUpperCase())
    .trim()
}

const formatValue = (value) => {
  if (typeof value === 'number') {
    return value.toLocaleString('fr-FR')
  }
  if (typeof value === 'boolean') {
    return value ? 'Oui' : 'Non'
  }
  return value
}
</script>

<style scoped>
.score-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.score-card--compact {
  padding: 1rem;
}

.score-card--excellent {
  border-color: #10b981;
}

.score-card--good {
  border-color: #3b82f6;
}

.score-card--average {
  border-color: #f59e0b;
}

.score-card--poor {
  border-color: #ef4444;
}

.score-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.score-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.score-icon--excellent {
  background: #d1fae5;
  color: #10b981;
}

.score-icon--good {
  background: #dbeafe;
  color: #3b82f6;
}

.score-icon--average {
  background: #fed7aa;
  color: #f59e0b;
}

.score-icon--poor {
  background: #fee2e2;
  color: #ef4444;
}

.score-info {
  flex: 1;
}

.score-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.25rem 0;
}

.score-subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.score-content {
  margin-bottom: 1rem;
}

.score-value {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.score-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
}

.score-max {
  font-size: 1.125rem;
  color: #6b7280;
  font-weight: 500;
}

.score-progress {
  margin-bottom: 1rem;
}

.score-track {
  width: 100%;
  height: 0.5rem;
  background: #f3f4f6;
  border-radius: 0.25rem;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  border-radius: 0.25rem;
  transition: width 0.5s ease;
}

.score-fill--excellent {
  background: linear-gradient(90deg, #10b981, #059669);
}

.score-fill--good {
  background: linear-gradient(90deg, #3b82f6, #2563eb);
}

.score-fill--average {
  background: linear-gradient(90deg, #f59e0b, #d97706);
}

.score-fill--poor {
  background: linear-gradient(90deg, #ef4444, #dc2626);
}

.score-description {
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.score-recommendations {
  margin-bottom: 1rem;
}

.recommendations-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 0.5rem 0;
}

.recommendations-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommendation-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: 0.25rem;
}

.recommendation-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.score-footer {
  border-top: 1px solid #f3f4f6;
  padding-top: 1rem;
}

.details-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #3b82f6;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s ease;
}

.details-btn:hover {
  color: #2563eb;
}

.rotate-180 {
  transform: rotate(180deg);
}

.score-details {
  border-top: 1px solid #f3f4f6;
  padding-top: 1rem;
  margin-top: 1rem;
}

.details-content {
  display: grid;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f9fafb;
}

.detail-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.detail-value {
  font-size: 0.875rem;
  font-weight: 500;
  color: #1f2937;
}
</style>
