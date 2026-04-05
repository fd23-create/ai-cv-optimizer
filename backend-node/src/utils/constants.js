// HTTP Status Codes
module.exports.STATUS_CODES = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  TOO_MANY_REQUESTS: 429,
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503
}

// Error Messages
module.exports.ERROR_MESSAGES = {
  // General
  INTERNAL_SERVER_ERROR: 'Une erreur interne est survenue',
  VALIDATION_ERROR: 'Erreur de validation des données',
  NOT_FOUND: 'Ressource non trouvée',
  UNAUTHORIZED: 'Non autorisé',
  FORBIDDEN: 'Accès interdit',
  
  // Authentication
  INVALID_TOKEN: 'Token invalide',
  TOKEN_EXPIRED: 'Token expiré',
  MISSING_TOKEN: 'Token manquant',
  
  // Resume
  RESUME_NOT_FOUND: 'CV non trouvé',
  INVALID_FILE_TYPE: 'Type de fichier invalide',
  FILE_TOO_LARGE: 'Fichier trop volumineux',
  UPLOAD_FAILED: 'Échec du téléchargement',
  ANALYSIS_FAILED: 'Échec de l\'analyse',
  
  // User
  USER_NOT_FOUND: 'Utilisateur non trouvé',
  USER_ALREADY_EXISTS: 'Utilisateur déjà existant',
  
  // Billing
  PAYMENT_FAILED: 'Échec du paiement',
  SUBSCRIPTION_NOT_FOUND: 'Abonnement non trouvé',
  INSUFFICIENT_CREDITS: 'Crédits insuffisants'
}

// File Types
module.exports.FILE_TYPES = {
  PDF: 'application/pdf',
  DOC: 'application/msword',
  DOCX: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

// Analysis Categories
module.exports.ANALYSIS_CATEGORIES = {
  SKILLS: 'skills',
  EXPERIENCE: 'experience',
  EDUCATION: 'education',
  FORMAT: 'format',
  OVERALL: 'overall'
}

// Score Ranges
module.exports.SCORE_RANGES = {
  EXCELLENT: { min: 80, max: 100, label: 'Excellent' },
  GOOD: { min: 60, max: 79, label: 'Bon' },
  AVERAGE: { min: 40, max: 59, label: 'Moyen' },
  POOR: { min: 0, max: 39, label: 'Faible' }
}

// Subscription Plans
module.exports.SUBSCRIPTION_PLANS = {
  FREE: {
    id: 'free',
    name: 'Gratuit',
    price: 0,
    credits: 3,
    features: ['3 analyses par mois', 'Support basic']
  },
  PRO: {
    id: 'pro',
    name: 'Professionnel',
    price: 9.99,
    credits: 50,
    features: ['50 analyses par mois', 'Support prioritaire', 'Export PDF']
  },
  ENTERPRISE: {
    id: 'enterprise',
    name: 'Entreprise',
    price: 29.99,
    credits: 200,
    features: ['200 analyses par mois', 'API access', 'Support dédié', 'Custom branding']
  }
}

// Queue Jobs
module.exports.QUEUE_JOBS = {
  RESUME_ANALYSIS: 'resume-analysis',
  EMAIL_NOTIFICATION: 'email-notification',
  CLEANUP_TEMP_FILES: 'cleanup-temp-files',
  GENERATE_REPORT: 'generate-report'
}

// Cache Keys
module.exports.CACHE_KEYS = {
  USER_PROFILE: (userId) => `user:profile:${userId}`,
  RESUME_ANALYSIS: (resumeId) => `resume:analysis:${resumeId}`,
  USER_RESUMES: (userId) => `user:resumes:${userId}`,
  SUBSCRIPTION: (userId) => `subscription:${userId}`
}

// Time Constants
module.exports.TIME = {
  MINUTE: 60 * 1000,
  HOUR: 60 * 60 * 1000,
  DAY: 24 * 60 * 60 * 1000,
  WEEK: 7 * 24 * 60 * 60 * 1000,
  MONTH: 30 * 24 * 60 * 60 * 1000
}

// Validation Rules
module.exports.VALIDATION_RULES = {
  FILE_SIZE: {
    MAX: 10 * 1024 * 1024, // 10MB
    MIN: 1024 // 1KB
  },
  RESUME_NAME: {
    MIN_LENGTH: 1,
    MAX_LENGTH: 255
  },
  USER_NAME: {
    MIN_LENGTH: 2,
    MAX_LENGTH: 50
  },
  PASSWORD: {
    MIN_LENGTH: 8,
    MAX_LENGTH: 128
  }
}
