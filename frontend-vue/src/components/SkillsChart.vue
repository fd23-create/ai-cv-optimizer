<template>
  <div class="skills-chart">
    <div class="chart-header">
      <h3 class="chart-title">{{ title }}</h3>
      <div v-if="showToggle" class="chart-toggle">
        <button
          @click="toggleChartType"
          class="toggle-btn"
          :class="{ 'toggle-btn--active': chartType === 'radar' }"
        >
          <BarChart3 v-if="chartType === 'bar'" />
          <Radar v-else />
        </button>
      </div>
    </div>
    
    <div class="chart-container" :class="`chart-container--${chartType}`">
      <canvas ref="chartCanvas" :width="width" :height="height"></canvas>
    </div>
    
    <div v-if="showLegend && skills.length > 0" class="chart-legend">
      <div class="legend-grid">
        <div
          v-for="(skill, index) in skills"
          :key="skill.name"
          class="legend-item"
        >
          <div
            class="legend-color"
            :style="{ backgroundColor: getSkillColor(index) }"
          ></div>
          <span class="legend-label">{{ skill.name }}</span>
          <span class="legend-value">{{ skill.level }}%</span>
        </div>
      </div>
    </div>
    
    <div v-if="skills.length === 0" class="chart-empty">
      <div class="empty-icon">
        <BarChart3 />
      </div>
      <p class="empty-text">Aucune compétence à afficher</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { BarChart3, Radar } from 'lucide-vue-next'

Chart.register(...registerables)

const props = defineProps({
  skills: {
    type: Array,
    default: () => [],
    validator: (skills) => skills.every(skill => 
      typeof skill.name === 'string' && 
      typeof skill.level === 'number' && 
      skill.level >= 0 && 
      skill.level <= 100
    )
  },
  title: {
    type: String,
    default: 'Compétences'
  },
  chartType: {
    type: String,
    default: 'bar',
    validator: (value) => ['bar', 'radar'].includes(value)
  },
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 300
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  showToggle: {
    type: Boolean,
    default: true
  },
  maxSkills: {
    type: Number,
    default: 10
  }
})

const emit = defineEmits(['skill-click'])

const chartCanvas = ref(null)
const chartInstance = ref(null)
const currentChartType = ref(props.chartType)

const colorPalette = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1'
]

const getSkillColor = (index) => {
  return colorPalette[index % colorPalette.length]
}

const createChartData = () => {
  const limitedSkills = props.skills.slice(0, props.maxSkills)
  
  return {
    labels: limitedSkills.map(skill => skill.name),
    datasets: [{
      label: 'Niveau de compétence',
      data: limitedSkills.map(skill => skill.level),
      backgroundColor: limitedSkills.map((_, index) => 
        getSkillColor(index) + '80' // Add transparency
      ),
      borderColor: limitedSkills.map((_, index) => getSkillColor(index)),
      borderWidth: 2,
      borderRadius: currentChartType.value === 'bar' ? 8 : 0,
      hoverBackgroundColor: limitedSkills.map((_, index) => 
        getSkillColor(index) + 'CC' // Darker on hover
      )
    }]
  }
}

const getChartOptions = () => {
  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false // We use custom legend
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        padding: 12,
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#fff',
        borderWidth: 1,
        displayColors: true,
        callbacks: {
          label: (context) => {
            return `${context.label}: ${context.parsed.y || context.parsed.r}%`
          }
        }
      }
    },
    onClick: (event, elements) => {
      if (elements.length > 0) {
        const index = elements[0].index
        const skill = props.skills[index]
        emit('skill-click', skill)
      }
    }
  }

  if (currentChartType.value === 'bar') {
    return {
      ...baseOptions,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            callback: (value) => `${value}%`
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          }
        },
        x: {
          grid: {
            display: false
          }
        }
      }
    }
  } else {
    return {
      ...baseOptions,
      scales: {
        r: {
          beginAtZero: true,
          max: 100,
          ticks: {
            stepSize: 20,
            callback: (value) => `${value}%`
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          pointLabels: {
            font: {
              size: 12
            }
          }
        }
      }
    }
  }
}

const createChart = () => {
  if (!chartCanvas.value) return

  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance.value = new Chart(ctx, {
    type: currentChartType.value,
    data: createChartData(),
    options: getChartOptions()
  })
}

const updateChart = () => {
  if (chartInstance.value) {
    chartInstance.value.data = createChartData()
    chartInstance.value.options = getChartOptions()
    chartInstance.value.update()
  }
}

const toggleChartType = () => {
  currentChartType.value = currentChartType.value === 'bar' ? 'radar' : 'bar'
  nextTick(() => {
    createChart()
  })
}

watch(() => props.skills, () => {
  updateChart()
}, { deep: true })

watch(() => props.chartType, (newType) => {
  currentChartType.value = newType
  nextTick(() => {
    createChart()
  })
})

onMounted(() => {
  nextTick(() => {
    createChart()
  })
})
</script>

<style scoped>
.skills-chart {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.chart-toggle {
  display: flex;
}

.toggle-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  background: white;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.toggle-btn--active {
  background: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
  margin-bottom: 1rem;
}

.chart-legend {
  margin-top: 1rem;
}

.legend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.75rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  flex-shrink: 0;
}

.legend-label {
  color: #4b5563;
  flex: 1;
}

.legend-value {
  color: #1f2937;
  font-weight: 500;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #9ca3af;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-text {
  font-size: 0.875rem;
  margin: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .chart-container {
    height: 250px;
  }
  
  .legend-grid {
    grid-template-columns: 1fr;
  }
}
</style>
