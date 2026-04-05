const winston = require('winston')
const path = require('path')

// Create logs directory if it doesn't exist
const logDir = path.join(__dirname, '../../logs')
require('fs').mkdirSync(logDir, { recursive: true })

// Define log format
const logFormat = winston.format.combine(
  winston.format.timestamp({
    format: 'YYYY-MM-DD HH:mm:ss'
  }),
  winston.format.errors({ stack: true }),
  winston.format.json(),
  winston.format.prettyPrint()
)

// Create logger instance
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  defaultMeta: { service: 'ai-cv-optimizer-backend' },
  transports: [
    // Write all logs with importance level of `error` or less to `error.log`
    new winston.transports.File({
      filename: path.join(logDir, 'error.log'),
      level: 'error',
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    }),
    
    // Write all logs with importance level of `info` or less to `combined.log`
    new winston.transports.File({
      filename: path.join(logDir, 'combined.log'),
      maxsize: 5242880, // 5MB
      maxFiles: 5,
    })
  ],
})

// If we're not in production, log to the console with a simple format
if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple(),
      winston.format.printf(({ timestamp, level, message, ...meta }) => {
        let msg = `${timestamp} [${level}]: ${message}`
        
        // Add metadata if present
        if (Object.keys(meta).length > 0) {
          msg += ' ' + JSON.stringify(meta)
        }
        
        return msg
      })
    )
  }))
}

// Add request logging helper
logger.logRequest = (req, res, next) => {
  const start = Date.now()
  
  res.on('finish', () => {
    const duration = Date.now() - start
    const logData = {
      method: req.method,
      url: req.originalUrl,
      status: res.statusCode,
      duration: `${duration}ms`,
      userAgent: req.get('User-Agent'),
      ip: req.ip || req.connection.remoteAddress
    }
    
    if (res.statusCode >= 400) {
      logger.warn('HTTP Request', logData)
    } else {
      logger.info('HTTP Request', logData)
    }
  })
  
  next()
}

// Add database query logging helper
logger.logQuery = (query, params, duration) => {
  logger.debug('Database Query', {
    query: query.substring(0, 200) + (query.length > 200 ? '...' : ''),
    params: params ? JSON.stringify(params).substring(0, 100) : null,
    duration: `${duration}ms`
  })
}

// Add ML service logging helper
logger.logMLService = (endpoint, payload, response, duration) => {
  logger.info('ML Service Call', {
    endpoint,
    payloadSize: JSON.stringify(payload).length,
    responseSize: JSON.stringify(response).length,
    duration: `${duration}ms`
  })
}

module.exports = logger
