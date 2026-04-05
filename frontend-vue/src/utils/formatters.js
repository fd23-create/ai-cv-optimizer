export const formatters = {
  formatDate(date) {
    if (!date) return ''
    
    const d = new Date(date)
    const options = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }
    
    return d.toLocaleDateString('fr-FR', options)
  },

  formatDateShort(date) {
    if (!date) return ''
    
    const d = new Date(date)
    const options = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    }
    
    return d.toLocaleDateString('fr-FR', options)
  },

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes'
    
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  },

  formatScore(score) {
    if (typeof score !== 'number') return '0%'
    return Math.round(score) + '%'
  },

  formatDuration(milliseconds) {
    if (!milliseconds) return '0s'
    
    const seconds = Math.floor(milliseconds / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(minutes / 60)
    
    if (hours > 0) {
      return `${hours}h ${minutes % 60}m`
    } else if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`
    } else {
      return `${seconds}s`
    }
  },

  formatCurrency(amount, currency = 'EUR') {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency
    }).format(amount)
  },

  formatPhoneNumber(phone) {
    const cleaned = phone.replace(/\D/g, '')
    const match = cleaned.match(/^(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})$/)
    
    if (match) {
      return `${match[1]} ${match[2]} ${match[3]} ${match[4]} ${match[5]}`
    }
    
    return phone
  },

  capitalizeFirst(str) {
    if (!str) return ''
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
  },

  truncateText(text, maxLength = 100) {
    if (!text || text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  },

  slugify(text) {
    return text
      .toString()
      .toLowerCase()
      .trim()
      .replace(/\s+/g, '-')
      .replace(/[^\w\-]+/g, '')
      .replace(/\-\-+/g, '-')
      .replace(/^-+/, '')
      .replace(/-+$/, '')
  },

  formatRelativeTime(date) {
    if (!date) return ''
    
    const now = new Date()
    const past = new Date(date)
    const diffInSeconds = Math.floor((now - past) / 1000)
    
    if (diffInSeconds < 60) {
      return 'à l\'instant'
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60)
      return `il y a ${minutes} minute${minutes > 1 ? 's' : ''}`
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600)
      return `il y a ${hours} heure${hours > 1 ? 's' : ''}`
    } else if (diffInSeconds < 2592000) {
      const days = Math.floor(diffInSeconds / 86400)
      return `il y a ${days} jour${days > 1 ? 's' : ''}`
    } else {
      return this.formatDateShort(date)
    }
  }
}
