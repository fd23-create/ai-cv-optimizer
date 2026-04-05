const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const morgan = require('morgan')
const rateLimit = require('express-rate-limit')
require('dotenv').config()

const logger = require('./utils/logger')
const errorHandler = require('./middlewares/errorHandler')
const authRoutes = require('./routes/auth')
const resumeRoutes = require('./routes/resumes')
const billingRoutes = require('./routes/billing')
const webhookRoutes = require('./routes/webhooks')

const app = express()

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}))

// CORS configuration
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? ['https://your-domain.com'] 
    : ['http://localhost:3000', 'http://localhost:8080'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}))

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS) || 15 * 60 * 1000, // 15 minutes
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS) || 100, // limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.'
  },
  standardHeaders: true,
  legacyHeaders: false,
})

app.use('/api/', limiter)

// Body parsing middleware
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// Logging middleware
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}))

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV,
    version: process.env.npm_package_version || '1.0.0'
  })
})

// API Routes
app.use('/api/auth', authRoutes)
app.use('/api/resumes', resumeRoutes)
app.use('/api/billing', billingRoutes)
app.use('/api/webhooks', webhookRoutes)

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    message: `Cannot ${req.method} ${req.originalUrl}`
  })
})

// Error handling middleware (must be last)
app.use(errorHandler)

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully')
  process.exit(0)
})

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully')
  process.exit(0)
})

// Unhandled promise rejection handler
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason)
})

// Uncaught exception handler
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error)
  process.exit(1)
})

const PORT = process.env.PORT || 5000

const server = app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT} in ${process.env.NODE_ENV} mode`)
  logger.info(`Health check available at http://localhost:${PORT}/health`)
})

module.exports = app
