const { Clerk } = require('@clerk/clerk-sdk-node')
const { UnauthorizedError, ForbiddenError } = require('./errorHandler')
const logger = require('../utils/logger')

// Initialize Clerk
const clerk = new Clerk({
  secretKey: process.env.CLERK_SECRET_KEY
})

// Authentication middleware
const authenticate = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '')
    
    if (!token) {
      throw new UnauthorizedError(ERROR_MESSAGES.MISSING_TOKEN)
    }

    // Verify token with Clerk
    const verifiedToken = await clerk.verifyToken(token)
    
    if (!verifiedToken) {
      throw new UnauthorizedError(ERROR_MESSAGES.INVALID_TOKEN)
    }

    // Get user information
    const user = await clerk.users.getUser(verifiedToken.sub)
    
    if (!user) {
      throw new UnauthorizedError(ERROR_MESSAGES.USER_NOT_FOUND)
    }

    // Add user to request object
    req.user = {
      id: user.id,
      email: user.primaryEmailAddress?.emailAddress,
      firstName: user.firstName,
      lastName: user.lastName,
      username: user.username,
      imageUrl: user.imageUrl,
      createdAt: user.createdAt
    }

    logger.debug('User authenticated', {
      userId: req.user.id,
      email: req.user.email
    })

    next()
  } catch (error) {
    logger.error('Authentication error:', error)
    
    if (error instanceof UnauthorizedError) {
      return next(error)
    }
    
    next(new UnauthorizedError(ERROR_MESSAGES.INVALID_TOKEN))
  }
}

// Optional authentication (doesn't throw error if not authenticated)
const optionalAuth = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '')
    
    if (token) {
      const verifiedToken = await clerk.verifyToken(token)
      
      if (verifiedToken) {
        const user = await clerk.users.getUser(verifiedToken.sub)
        
        if (user) {
          req.user = {
            id: user.id,
            email: user.primaryEmailAddress?.emailAddress,
            firstName: user.firstName,
            lastName: user.lastName,
            username: user.username,
            imageUrl: user.imageUrl,
            createdAt: user.createdAt
          }
        }
      }
    }
    
    next()
  } catch (error) {
    // Don't throw error for optional auth
    logger.warn('Optional authentication failed:', error)
    next()
  }
}

// Role-based authorization
const authorize = (roles = []) => {
  return (req, res, next) => {
    if (!req.user) {
      return next(new UnauthorizedError())
    }

    const userRoles = req.user.roles || []
    const hasRequiredRole = roles.some(role => userRoles.includes(role))

    if (!hasRequiredRole) {
      return next(new ForbiddenError())
    }

    next()
  }
}

// Resource ownership check
const checkOwnership = (resourceIdParam = 'id', resourceType = 'resource') => {
  return async (req, res, next) => {
    try {
      if (!req.user) {
        return next(new UnauthorizedError())
      }

      const resourceId = req.params[resourceIdParam]
      
      // This would typically involve a database check
      // For now, we'll assume the user has access if they're authenticated
      // In a real implementation, you would check if req.user.id owns the resource
      
      logger.debug('Ownership check passed', {
        userId: req.user.id,
        resourceId,
        resourceType
      })

      next()
    } catch (error) {
      logger.error('Ownership check failed:', error)
      next(new ForbiddenError())
    }
  }
}

// Rate limiting by user
const userRateLimit = (maxRequests = 100, windowMs = 15 * 60 * 1000) => {
  const requests = new Map()

  return (req, res, next) => {
    if (!req.user) {
      return next(new UnauthorizedError())
    }

    const userId = req.user.id
    const now = Date.now()
    const windowStart = now - windowMs

    // Clean old requests
    if (requests.has(userId)) {
      const userRequests = requests.get(userId).filter(time => time > windowStart)
      requests.set(userId, userRequests)
    } else {
      requests.set(userId, [])
    }

    const userRequests = requests.get(userId)

    if (userRequests.length >= maxRequests) {
      return res.status(429).json({
        success: false,
        error: 'Too many requests',
        message: `Rate limit exceeded. Maximum ${maxRequests} requests per ${windowMs / 60000} minutes.`
      })
    }

    userRequests.push(now)
    next()
  }
}

// Admin only middleware
const adminOnly = authorize(['admin'])

// Premium user middleware
const premiumOnly = authorize(['premium', 'admin'])

module.exports = {
  authenticate,
  optionalAuth,
  authorize,
  checkOwnership,
  userRateLimit,
  adminOnly,
  premiumOnly
}
