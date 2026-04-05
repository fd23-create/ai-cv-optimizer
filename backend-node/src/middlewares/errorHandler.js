const logger = require('../utils/logger')
const { STATUS_CODES, ERROR_MESSAGES } = require('../utils/constants')

// Custom error classes
class AppError extends Error {
  constructor(message, statusCode) {
    super(message)
    this.statusCode = statusCode
    this.isOperational = true
    
    Error.captureStackTrace(this, this.constructor)
  }
}

class ValidationError extends AppError {
  constructor(message, details = null) {
    super(message, STATUS_CODES.UNPROCESSABLE_ENTITY)
    this.details = details
  }
}

class NotFoundError extends AppError {
  constructor(resource = 'Ressource') {
    super(`${resource} non trouvée`, STATUS_CODES.NOT_FOUND)
  }
}

class UnauthorizedError extends AppError {
  constructor(message = ERROR_MESSAGES.UNAUTHORIZED) {
    super(message, STATUS_CODES.UNAUTHORIZED)
  }
}

class ForbiddenError extends AppError {
  constructor(message = ERROR_MESSAGES.FORBIDDEN) {
    super(message, STATUS_CODES.FORBIDDEN)
  }
}

class ConflictError extends AppError {
  constructor(message) {
    super(message, STATUS_CODES.CONFLICT)
  }
}

// Error handling middleware
const errorHandler = (err, req, res, next) => {
  let error = { ...err }
  error.message = err.message

  // Log error
  logger.error('Error occurred:', {
    error: err.message,
    stack: err.stack,
    url: req.originalUrl,
    method: req.method,
    ip: req.ip,
    userAgent: req.get('User-Agent')
  })

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    const message = 'Ressource non trouvée'
    error = new AppError(message, STATUS_CODES.NOT_FOUND)
  }

  // Mongoose duplicate key
  if (err.code === 11000) {
    const message = 'Cette ressource existe déjà'
    error = new ConflictError(message)
  }

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const message = 'Erreur de validation des données'
    const details = Object.values(err.errors).map(val => ({
      field: val.path,
      message: val.message
    }))
    error = new ValidationError(message, details)
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    const message = ERROR_MESSAGES.INVALID_TOKEN
    error = new UnauthorizedError(message)
  }

  if (err.name === 'TokenExpiredError') {
    const message = ERROR_MESSAGES.TOKEN_EXPIRED
    error = new UnauthorizedError(message)
  }

  // Multer errors
  if (err.code === 'LIMIT_FILE_SIZE') {
    const message = ERROR_MESSAGES.FILE_TOO_LARGE
    error = new ValidationError(message)
  }

  if (err.code === 'LIMIT_FILE_COUNT') {
    const message = 'Trop de fichiers'
    error = new ValidationError(message)
  }

  if (err.code === 'LIMIT_UNEXPECTED_FILE') {
    const message = 'Champ de fichier inattendu'
    error = new ValidationError(message)
  }

  // Joi validation errors
  if (err.isJoi) {
    const message = ERROR_MESSAGES.VALIDATION_ERROR
    const details = err.details.map(detail => ({
      field: detail.path.join('.'),
      message: detail.message
    }))
    error = new ValidationError(message, details)
  }

  // Default error response
  const response = {
    success: false,
    error: error.message || ERROR_MESSAGES.INTERNAL_SERVER_ERROR,
    timestamp: new Date().toISOString(),
    path: req.originalUrl
  }

  // Add validation details if available
  if (error.details) {
    response.details = error.details
  }

  // Add stack trace in development
  if (process.env.NODE_ENV === 'development') {
    response.stack = err.stack
  }

  res.status(error.statusCode || STATUS_CODES.INTERNAL_SERVER_ERROR).json(response)
}

// Async error wrapper
const asyncHandler = (fn) => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}

// 404 handler
const notFound = (req, res, next) => {
  const error = new NotFoundError('Route')
  next(error)
}

module.exports = {
  errorHandler,
  asyncHandler,
  notFound,
  AppError,
  ValidationError,
  NotFoundError,
  UnauthorizedError,
  ForbiddenError,
  ConflictError
}
