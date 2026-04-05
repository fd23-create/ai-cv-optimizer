/**
 * HTTP Status Codes and API Response Codes
 * Shared constants for frontend and backend services
 */

/**
 * HTTP Status Codes
 */
export const HTTP_STATUS = {
  // Success codes
  OK: 200,
  CREATED: 201,
  ACCEPTED: 202,
  NO_CONTENT: 204,
  
  // Redirection codes
  MOVED_PERMANENTLY: 301,
  FOUND: 302,
  NOT_MODIFIED: 304,
  
  // Client error codes
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  METHOD_NOT_ALLOWED: 405,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  TOO_MANY_REQUESTS: 429,
  
  // Server error codes
  INTERNAL_SERVER_ERROR: 500,
  NOT_IMPLEMENTED: 501,
  BAD_GATEWAY: 502,
  SERVICE_UNAVAILABLE: 503,
  GATEWAY_TIMEOUT: 504
};

/**
 * Application-specific error codes
 */
export const ERROR_CODES = {
  // General errors
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  CONFLICT: 'CONFLICT',
  
  // Authentication errors
  INVALID_TOKEN: 'INVALID_TOKEN',
  TOKEN_EXPIRED: 'TOKEN_EXPIRED',
  MISSING_TOKEN: 'MISSING_TOKEN',
  INVALID_CREDENTIALS: 'INVALID_CREDENTIALS',
  ACCOUNT_LOCKED: 'ACCOUNT_LOCKED',
  
  // Resume errors
  RESUME_NOT_FOUND: 'RESUME_NOT_FOUND',
  INVALID_FILE_TYPE: 'INVALID_FILE_TYPE',
  FILE_TOO_LARGE: 'FILE_TOO_LARGE',
  FILE_TOO_SMALL: 'FILE_TOO_SMALL',
  UPLOAD_FAILED: 'UPLOAD_FAILED',
  PROCESSING_FAILED: 'PROCESSING_FAILED',
  ANALYSIS_FAILED: 'ANALYSIS_FAILED',
  EXTRACTION_FAILED: 'EXTRACTION_FAILED',
  
  // User errors
  USER_NOT_FOUND: 'USER_NOT_FOUND',
  USER_ALREADY_EXISTS: 'USER_ALREADY_EXISTS',
  USER_NOT_VERIFIED: 'USER_NOT_VERIFIED',
  USER_SUSPENDED: 'USER_SUSPENDED',
  
  // Subscription/Billing errors
  SUBSCRIPTION_NOT_FOUND: 'SUBSCRIPTION_NOT_FOUND',
  SUBSCRIPTION_EXPIRED: 'SUBSCRIPTION_EXPIRED',
  PAYMENT_FAILED: 'PAYMENT_FAILED',
  INSUFFICIENT_CREDITS: 'INSUFFICIENT_CREDITS',
  PLAN_NOT_AVAILABLE: 'PLAN_NOT_AVAILABLE',
  
  // Rate limiting errors
  RATE_LIMIT_EXCEEDED: 'RATE_LIMIT_EXCEEDED',
  QUOTA_EXCEEDED: 'QUOTA_EXCEEDED',
  
  // Service errors
  SERVICE_UNAVAILABLE: 'SERVICE_UNAVAILABLE',
  EXTERNAL_SERVICE_ERROR: 'EXTERNAL_SERVICE_ERROR',
  DATABASE_ERROR: 'DATABASE_ERROR',
  CACHE_ERROR: 'CACHE_ERROR',
  
  // File processing errors
  CORRUPTED_FILE: 'CORRUPTED_FILE',
  UNSUPPORTED_FORMAT: 'UNSUPPORTED_FORMAT',
  ENCRYPTION_ERROR: 'ENCRYPTION_ERROR',
  
  // AI/ML service errors
  ML_SERVICE_ERROR: 'ML_SERVICE_ERROR',
  MODEL_NOT_AVAILABLE: 'MODEL_NOT_AVAILABLE',
  ANALYSIS_TIMEOUT: 'ANALYSIS_TIMEOUT',
  INVALID_INPUT_FORMAT: 'INVALID_INPUT_FORMAT'
};

/**
 * Resume processing status codes
 */
export const RESUME_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
  RETRYING: 'retrying'
};

/**
 * Analysis status codes
 */
export const ANALYSIS_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
  TIMEOUT: 'timeout'
};

/**
 * User account status codes
 */
export const USER_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive',
  SUSPENDED: 'suspended',
  PENDING_VERIFICATION: 'pending_verification',
  DELETED: 'deleted'
};

/**
 * Subscription status codes
 */
export const SUBSCRIPTION_STATUS = {
  ACTIVE: 'active',
  EXPIRED: 'expired',
  CANCELLED: 'cancelled',
  PENDING: 'pending',
  PAST_DUE: 'past_due'
};

/**
 * Payment status codes
 */
export const PAYMENT_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
  REFUNDED: 'refunded',
  PARTIALLY_REFUNDED: 'partially_refunded'
};

/**
 * File type codes
 */
export const FILE_TYPES = {
  PDF: 'pdf',
  DOC: 'doc',
  DOCX: 'docx',
  TXT: 'txt',
  RTF: 'rtf'
};

/**
 * MIME type mappings
 */
export const MIME_TYPES = {
  [FILE_TYPES.PDF]: 'application/pdf',
  [FILE_TYPES.DOC]: 'application/msword',
  [FILE_TYPES.DOCX]: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  [FILE_TYPES.TXT]: 'text/plain',
  [FILE_TYPES.RTF]: 'application/rtf'
};

/**
 * Supported language codes
 */
export const SUPPORTED_LANGUAGES = {
  ENGLISH: 'en',
  FRENCH: 'fr',
  SPANISH: 'es',
  GERMAN: 'de',
  ITALIAN: 'it',
  PORTUGUESE: 'pt'
};

/**
 * Skill categories
 */
export const SKILL_CATEGORIES = {
  TECHNICAL: 'technical',
  BUSINESS: 'business',
  SOFT_SKILLS: 'soft_skills',
  TOOLS: 'tools'
};

/**
 * Skill subcategories
 */
export const SKILL_SUBCATEGORIES = {
  // Technical
  PROGRAMMING: 'programming',
  WEB_DEVELOPMENT: 'web_development',
  DATABASES: 'databases',
  CLOUD: 'cloud',
  DATA_SCIENCE: 'data_science',
  MOBILE: 'mobile',
  DEVOPS: 'devops',
  
  // Business
  MANAGEMENT: 'management',
  MARKETING: 'marketing',
  SALES: 'sales',
  FINANCE: 'finance',
  OPERATIONS: 'operations',
  
  // Soft Skills
  COMMUNICATION: 'communication',
  LEADERSHIP: 'leadership',
  PROBLEM_SOLVING: 'problem_solving',
  COLLABORATION: 'collaboration',
  ADAPTABILITY: 'adaptability',
  
  // Tools
  OFFICE: 'office',
  DESIGN: 'design',
  DEVELOPMENT_TOOLS: 'development_tools',
  ANALYTICS: 'analytics'
};

/**
 * Education levels
 */
export const EDUCATION_LEVELS = {
  HIGH_SCHOOL: 'high_school',
  ASSOCIATE: 'associate',
  BACHELOR: 'bachelor',
  LICENCE: 'licence',
  MASTER: 'master',
  MBA: 'mba',
  PHD: 'phd',
  DOCTORATE: 'doctorate',
  POSTDOC: 'postdoc'
};

/**
 * Score ranges and levels
 */
export const SCORE_RANGES = {
  EXCELLENT: { min: 90, max: 100, label: 'Excellent', color: '#10b981' },
  VERY_GOOD: { min: 80, max: 89, label: 'Very Good', color: '#3b82f6' },
  GOOD: { min: 70, max: 79, label: 'Good', color: '#3b82f6' },
  AVERAGE: { min: 60, max: 69, label: 'Average', color: '#f59e0b' },
  BELOW_AVERAGE: { min: 50, max: 59, label: 'Below Average', color: '#f59e0b' },
  POOR: { min: 0, max: 49, label: 'Poor', color: '#ef4444' }
};

/**
 * Career progression levels
 */
export const CAREER_PROGRESSION = {
  STRONG: 'strong',
  MODERATE: 'moderate',
  WEAK: 'weak',
  STAGNANT: 'stagnant',
  UNKNOWN: 'unknown'
};

/**
 * Industry categories
 */
export const INDUSTRIES = {
  TECHNOLOGY: 'technology',
  HEALTHCARE: 'healthcare',
  FINANCE: 'finance',
  MARKETING: 'marketing',
  EDUCATION: 'education',
  CONSULTING: 'consulting',
  MANUFACTURING: 'manufacturing',
  RETAIL: 'retail',
  GOVERNMENT: 'government',
  NON_PROFIT: 'non_profit'
};

/**
 * Subscription plans
 */
export const SUBSCRIPTION_PLANS = {
  FREE: 'free',
  PRO: 'pro',
  ENTERPRISE: 'enterprise'
};

/**
 * Queue job types
 */
export const QUEUE_JOBS = {
  RESUME_ANALYSIS: 'resume-analysis',
  RESUME_UPLOAD: 'resume-upload',
  EMAIL_NOTIFICATION: 'email-notification',
  REPORT_GENERATION: 'report-generation',
  CLEANUP_TEMP_FILES: 'cleanup-temp-files',
  USER_SYNC: 'user-sync',
  SUBSCRIPTION_RENEWAL: 'subscription-renewal'
};

/**
 * Cache key patterns
 */
export const CACHE_KEYS = {
  USER_PROFILE: (userId) => `user:profile:${userId}`,
  RESUME_ANALYSIS: (resumeId) => `resume:analysis:${resumeId}`,
  USER_RESUMES: (userId) => `user:resumes:${userId}`,
  USER_SUBSCRIPTION: (userId) => `user:subscription:${userId}`,
  SKILL_SUGGESTIONS: (userId, industry) => `skills:suggestions:${userId}:${industry}`,
  ANALYSIS_QUEUE: 'analysis:queue',
  RATE_LIMIT: (userId, endpoint) => `rate_limit:${userId}:${endpoint}`
};

/**
 * Time constants (in milliseconds)
 */
export const TIME = {
  SECOND: 1000,
  MINUTE: 60 * 1000,
  HOUR: 60 * 60 * 1000,
  DAY: 24 * 60 * 60 * 1000,
  WEEK: 7 * 24 * 60 * 60 * 1000,
  MONTH: 30 * 24 * 60 * 60 * 1000,
  YEAR: 365 * 24 * 60 * 60 * 1000
};

/**
 * File size limits (in bytes)
 */
export const FILE_SIZE_LIMITS = {
  MIN: 1024, // 1KB
  MAX: 10 * 1024 * 1024, // 10MB
  MAX_TEXT_LENGTH: 50000, // 50KB of text
  MAX_SKILLS: 100,
  MAX_EXPERIENCE: 20,
  MAX_EDUCATION: 10
};

/**
 * Validation limits
 */
export const VALIDATION_LIMITS = {
  RESUME_NAME: { min: 1, max: 255 },
  DESCRIPTION: { min: 0, max: 1000 },
  TARGET_JOB: { min: 0, max: 100 },
  INDUSTRY: { min: 0, max: 50 },
  TAGS: { max: 10, maxLength: 50 },
  SKILL_NAME: { min: 2, max: 100 },
  EXPERIENCE_TITLE: { min: 2, max: 200 },
  EXPERIENCE_DESCRIPTION: { max: 2000 },
  EDUCATION_DEGREE: { max: 200 },
  EDUCATION_FIELD: { max: 200 }
};

/**
 * API rate limits
 */
export const RATE_LIMITS = {
  UPLOAD: { requests: 5, window: TIME.MINUTE },
  ANALYSIS: { requests: 10, window: TIME.MINUTE },
  DOWNLOAD: { requests: 20, window: TIME.MINUTE },
  SEARCH: { requests: 100, window: TIME.MINUTE },
  GENERAL: { requests: 1000, window: TIME.HOUR }
};

/**
 * Notification types
 */
export const NOTIFICATION_TYPES = {
  INFO: 'info',
  SUCCESS: 'success',
  WARNING: 'warning',
  ERROR: 'error'
};

/**
 * Log levels
 */
export const LOG_LEVELS = {
  ERROR: 'error',
  WARN: 'warn',
  INFO: 'info',
  DEBUG: 'debug'
};

/**
 * Export formats
 */
export const EXPORT_FORMATS = {
  PDF: 'pdf',
  DOCX: 'docx',
  JSON: 'json',
  CSV: 'csv'
};

/**
 * Sorting options
 */
export const SORT_OPTIONS = {
  CREATED_AT: 'createdAt',
  UPDATED_AT: 'updatedAt',
  SCORE: 'score',
  FILE_NAME: 'fileName',
  FILE_SIZE: 'fileSize'
};

/**
 * Sort orders
 */
export const SORT_ORDERS = {
  ASC: 'asc',
  DESC: 'desc'
};

// For CommonJS environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    HTTP_STATUS,
    ERROR_CODES,
    RESUME_STATUS,
    ANALYSIS_STATUS,
    USER_STATUS,
    SUBSCRIPTION_STATUS,
    PAYMENT_STATUS,
    FILE_TYPES,
    MIME_TYPES,
    SUPPORTED_LANGUAGES,
    SKILL_CATEGORIES,
    SKILL_SUBCATEGORIES,
    EDUCATION_LEVELS,
    SCORE_RANGES,
    CAREER_PROGRESSION,
    INDUSTRIES,
    SUBSCRIPTION_PLANS,
    QUEUE_JOBS,
    CACHE_KEYS,
    TIME,
    FILE_SIZE_LIMITS,
    VALIDATION_LIMITS,
    RATE_LIMITS,
    NOTIFICATION_TYPES,
    LOG_LEVELS,
    EXPORT_FORMATS,
    SORT_OPTIONS,
    SORT_ORDERS
  };
}
