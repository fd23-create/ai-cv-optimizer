<template>
  <div class="upload-button">
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      @change="handleFileChange"
      class="file-input"
    />
    <button
      @click="triggerFileInput"
      :disabled="disabled || isLoading"
      class="upload-btn"
      :class="{
        'upload-btn--loading': isLoading,
        'upload-btn--disabled': disabled
      }"
    >
      <div v-if="isLoading" class="loading-content">
        <div class="spinner"></div>
        <span>{{ loadingText }}</span>
      </div>
      <div v-else class="default-content">
        <Upload class="icon" />
        <span>{{ buttonText }}</span>
      </div>
    </button>
    
    <div v-if="errors.length > 0" class="errors">
      <div v-for="error in errors" :key="error" class="error-item">
        <AlertCircle class="error-icon" />
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Upload, AlertCircle } from 'lucide-vue-next'
import { fileValidators } from '@/utils/validators.js'

const props = defineProps({
  accept: {
    type: String,
    default: '.pdf,.doc,.docx'
  },
  buttonText: {
    type: String,
    default: 'Choisir un fichier'
  },
  loadingText: {
    type: String,
    default: 'Téléchargement...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  maxSize: {
    type: Number,
    default: 10 * 1024 * 1024 // 10MB
  }
})

const emit = defineEmits(['file-selected', 'error', 'success'])

const fileInput = ref(null)
const errors = ref([])

const triggerFileInput = () => {
  if (!props.disabled && !props.isLoading) {
    fileInput.value?.click()
  }
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  errors.value = []

  if (!file) {
    emit('error', 'Aucun fichier sélectionné')
    return
  }

  const validation = fileValidators.validateResumeFile(file)
  
  if (!validation.isValid) {
    errors.value = validation.errors
    emit('error', validation.errors)
    return
  }

  emit('file-selected', file)
  emit('success', file)
  
  // Reset input
  event.target.value = ''
}

const clearErrors = () => {
  errors.value = []
}

defineExpose({
  clearErrors
})
</script>

<style scoped>
.upload-button {
  width: 100%;
}

.file-input {
  display: none;
}

.upload-btn {
  width: 100%;
  padding: 1rem 2rem;
  border: 2px dashed #cbd5e1;
  border-radius: 0.75rem;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-weight: 500;
  color: #64748b;
}

.upload-btn:hover:not(.upload-btn--disabled):not(.upload-btn--loading) {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #3b82f6;
}

.upload-btn--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upload-btn--loading {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #3b82f6;
}

.default-content,
.loading-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icon {
  width: 20px;
  height: 20px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #e2e8f0;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.errors {
  margin-top: 0.75rem;
}

.error-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #ef4444;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.error-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
</style>
