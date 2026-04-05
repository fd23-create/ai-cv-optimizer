const Joi = require('joi')
const { ValidationError } = require('./errorHandler')
const { FILE_TYPES, VALIDATION_RULES } = require('../utils/constants')

// Generic validation middleware
const validate = (schema, property = 'body') => {
  return (req, res, next) => {
    const { error, value } = schema.validate(req[property], {
      abortEarly: false,
      stripUnknown: true
    })

    if (error) {
      const details = error.details.map(detail => ({
        field: detail.path.join('.'),
        message: detail.message,
        value: detail.context?.value
      }))
      
      return next(new ValidationError('Validation failed', details))
    }

    req[property] = value
    next()
  }
}

// File validation middleware
const validateFile = (options = {}) => {
  const {
    required = true,
    maxSize = VALIDATION_RULES.FILE_SIZE.MAX,
    allowedTypes = Object.values(FILE_TYPES),
    maxFiles = 1
  } = options

  return (req, res, next) => {
    const files = req.files || (req.file ? [req.file] : [])

    if (required && files.length === 0) {
      return next(new ValidationError('File is required'))
    }

    if (files.length > maxFiles) {
      return next(new ValidationError(`Maximum ${maxFiles} files allowed`))
    }

    for (const file of files) {
      // Check file size
      if (file.size > maxSize) {
        return next(new ValidationError(`File size exceeds limit of ${maxSize / 1024 / 1024}MB`))
      }

      // Check file type
      if (!allowedTypes.includes(file.mimetype)) {
        return next(new ValidationError(`Invalid file type. Allowed types: ${allowedTypes.join(', ')}`))
      }
    }

    next()
  }
}

// Validation schemas
const schemas = {
  // User schemas
  userSync: Joi.object({
    clerkId: Joi.string().required(),
    email: Joi.string().email().required(),
    firstName: Joi.string().min(VALIDATION_RULES.USER_NAME.MIN_LENGTH).max(VALIDATION_RULES.USER_NAME.MAX_LENGTH).required(),
    lastName: Joi.string().min(VALIDATION_RULES.USER_NAME.MIN_LENGTH).max(VALIDATION_RULES.USER_NAME.MAX_LENGTH).required()
  }),

  // Resume schemas
  resumeUpload: Joi.object({
    title: Joi.string().min(VALIDATION_RULES.RESUME_NAME.MIN_LENGTH).max(VALIDATION_RULES.RESUME_NAME.MAX_LENGTH).optional(),
    description: Joi.string().max(500).optional(),
    targetJob: Joi.string().max(100).optional(),
    industry: Joi.string().max(50).optional()
  }),

  resumeUpdate: Joi.object({
    title: Joi.string().min(VALIDATION_RULES.RESUME_NAME.MIN_LENGTH).max(VALIDATION_RULES.RESUME_NAME.MAX_LENGTH).optional(),
    description: Joi.string().max(500).optional(),
    targetJob: Joi.string().max(100).optional(),
    industry: Joi.string().max(50).optional(),
    isPublic: Joi.boolean().optional()
  }),

  // Analysis schemas
  analysisRequest: Joi.object({
    options: Joi.object({
      includeSkills: Joi.boolean().default(true),
      includeExperience: Joi.boolean().default(true),
      includeEducation: Joi.boolean().default(true),
      includeFormat: Joi.boolean().default(true),
      customKeywords: Joi.array().items(Joi.string()).optional()
    }).optional()
  }),

  // Billing schemas
  createCheckoutSession: Joi.object({
    planId: Joi.string().valid('free', 'pro', 'enterprise').required(),
    successUrl: Joi.string().uri().required(),
    cancelUrl: Joi.string().uri().required()
  }),

  updateSubscription: Joi.object({
    planId: Joi.string().valid('pro', 'enterprise').required()
  }),

  // Query parameter schemas
  pagination: Joi.object({
    page: Joi.number().integer().min(1).default(1),
    limit: Joi.number().integer().min(1).max(100).default(20),
    sort: Joi.string().valid('createdAt', 'updatedAt', 'score', 'title').default('createdAt'),
    order: Joi.string().valid('asc', 'desc').default('desc')
  }),

  resumeFilters: Joi.object({
    status: Joi.string().valid('pending', 'processing', 'completed', 'failed').optional(),
    minScore: Joi.number().integer().min(0).max(100).optional(),
    maxScore: Joi.number().integer().min(0).max(100).optional(),
    industry: Joi.string().optional(),
    dateFrom: Joi.date().optional(),
    dateTo: Joi.date().optional()
  })
}

// Validation middleware functions
const validateUserSync = validate(schemas.userSync)

const validateResumeUpload = [
  validate(schemas.resumeUpload),
  validateFile({
    required: true,
    maxSize: VALIDATION_RULES.FILE_SIZE.MAX,
    allowedTypes: Object.values(FILE_TYPES),
    maxFiles: 1
  })
]

const validateResumeUpdate = validate(schemas.resumeUpdate)

const validateAnalysisRequest = validate(schemas.analysisRequest)

const validateCreateCheckoutSession = validate(schemas.createCheckoutSession)

const validateUpdateSubscription = validate(schemas.updateSubscription)

const validatePagination = (req, res, next) => {
  const { error, value } = schemas.pagination.validate(req.query, {
    abortEarly: false,
    stripUnknown: true
  })

  if (error) {
    const details = error.details.map(detail => ({
      field: detail.path.join('.'),
      message: detail.message
    }))
    
    return next(new ValidationError('Invalid pagination parameters', details))
  }

  req.query = { ...req.query, ...value }
  next()
}

const validateResumeFilters = (req, res, next) => {
  const { error, value } = schemas.resumeFilters.validate(req.query, {
    abortEarly: false,
    stripUnknown: true
  })

  if (error) {
    const details = error.details.map(detail => ({
      field: detail.path.join('.'),
      message: detail.message
    }))
    
    return next(new ValidationError('Invalid filter parameters', details))
  }

  req.query = { ...req.query, ...value }
  next()
}

// Custom validation functions
const validateObjectId = (paramName = 'id') => {
  return (req, res, next) => {
    const id = req.params[paramName]
    
    if (!id || typeof id !== 'string' || id.length !== 24) {
      return next(new ValidationError(`Invalid ${paramName}`))
    }
    
    next()
  }
}

const validateEmail = (email) => {
  const schema = Joi.string().email()
  const { error } = schema.validate(email)
  return !error
}

const validatePassword = (password) => {
  const schema = Joi.string()
    .min(VALIDATION_RULES.PASSWORD.MIN_LENGTH)
    .max(VALIDATION_RULES.PASSWORD.MAX_LENGTH)
    .pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
  
  const { error } = schema.validate(password)
  return !error
}

module.exports = {
  validate,
  validateFile,
  validateUserSync,
  validateResumeUpload,
  validateResumeUpdate,
  validateAnalysisRequest,
  validateCreateCheckoutSession,
  validateUpdateSubscription,
  validatePagination,
  validateResumeFilters,
  validateObjectId,
  validateEmail,
  validatePassword,
  schemas
}
