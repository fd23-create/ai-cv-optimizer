const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const morgan = require('morgan')
const rateLimit = require('express-rate-limit')
require('dotenv').config()

const logger = require('./utils/logger.simple')
const errorHandler = require('./middlewares/errorHandler.simple')

const app = express()

// Security middleware
app.use(helmet({
  contentSecurityPolicy: false, // Simplified for development
}))

// CORS configuration
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}))

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
})
app.use(limiter)

// Logging middleware
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } }))

// Body parsing middleware
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development'
  })
})

// API routes (placeholder)
app.get('/api', (req, res) => {
  res.json({
    message: 'AI CV Optimizer API',
    version: '1.0.0',
    endpoints: [
      'GET /health',
      'GET /api',
      'POST /api/resumes/upload (placeholder)',
      'GET /api/resumes (placeholder)'
    ]
  })
})

// Mock resume upload endpoint
app.post('/api/resumes/upload', (req, res) => {
  try {
    logger.info('Mock resume upload received')
    res.json({
      success: true,
      message: 'Resume uploaded successfully (mock mode)',
      data: {
        id: 'mock-resume-id',
        filename: 'mock-resume.pdf',
        status: 'uploaded'
      }
    })
  } catch (error) {
    logger.error('Mock upload error:', error)
    res.status(500).json({
      success: false,
      message: 'Upload failed'
    })
  }
})

// Mock analysis endpoint
app.post('/api/resumes/:id/analyze', (req, res) => {
  try {
    logger.info('Mock analysis requested')
    res.json({
      success: true,
      message: 'Analysis completed (mock mode)',
      data: {
        id: req.params.id,
        overallScore: 85,
        scores: {
          skills: 88,
          experience: 82,
          education: 90,
          format: 85
        },
        recommendations: [
          'Add more quantifiable achievements',
          'Include a professional summary'
        ]
      }
    })
  } catch (error) {
    logger.error('Mock analysis error:', error)
    res.status(500).json({
      success: false,
      message: 'Analysis failed'
    })
  }
})

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'Endpoint not found',
    path: req.originalUrl
  })
})

// Error handling middleware
app.use(errorHandler)

const PORT = process.env.PORT || 5000

const startServer = async () => {
  try {
    app.listen(PORT, () => {
      logger.info(`Server running on port ${PORT}`)
      logger.info(`Environment: ${process.env.NODE_ENV || 'development'}`)
      logger.info(`Health check: http://localhost:${PORT}/health`)
    })
  } catch (error) {
    logger.error('Failed to start server:', error)
    process.exit(1)
  }
}

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully')
  process.exit(0)
})

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully')
  process.exit(0)
})

startServer()

module.exports = app
