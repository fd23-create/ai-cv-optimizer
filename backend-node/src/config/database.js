const { createClient } = require('@supabase/supabase-js')
const logger = require('../utils/logger')

// Supabase configuration
const supabaseUrl = process.env.SUPABASE_URL
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY

let supabase = null

// Create Supabase client only if configuration is available
if (supabaseUrl && supabaseServiceKey && supabaseUrl !== 'https://your-project.supabase.co') {
  supabase = createClient(supabaseUrl, supabaseServiceKey, {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  })
} else {
  logger.warn('Supabase not configured - running in mock mode')
}

// Database connection test
const testConnection = async () => {
  if (!supabase) {
    logger.warn('Database connection skipped - running in mock mode')
    return true
  }
  
  try {
    const { data, error } = await supabase
      .from('profiles')
      .select('id')
      .limit(1)

    if (error) {
      throw error
    }

    logger.info('Database connection successful')
    return true
  } catch (error) {
    logger.error('Database connection failed:', error)
    return false
  }
}

// Database helper functions
const db = {
  // Generic query helper
  async query(table, options = {}) {
    const {
      select = '*',
      where = {},
      orderBy = { column: 'created_at', ascending: false },
      limit = null,
      offset = null,
      single = false
    } = options

    try {
      let query = supabase.from(table).select(select)

      // Apply filters
      Object.entries(where).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          query = query.in(key, value)
        } else if (typeof value === 'object' && value !== null) {
          // Handle complex filters like { operator: '>', value: 100 }
          const { operator, val } = value
          switch (operator) {
            case '>':
              query = query.gt(key, val)
              break
            case '>=':
              query = query.gte(key, val)
              break
            case '<':
              query = query.lt(key, val)
              break
            case '<=':
              query = query.lte(key, val)
              break
            case 'like':
              query = query.like(key, val)
              break
            case 'ilike':
              query = query.ilike(key, val)
              break
            default:
              query = query.eq(key, val)
          }
        } else {
          query = query.eq(key, value)
        }
      })

      // Apply ordering
      if (orderBy.column) {
        query = query.order(orderBy.column, { ascending: orderBy.ascending })
      }

      // Apply pagination
      if (limit) {
        query = query.limit(limit)
      }

      if (offset) {
        query = query.offset(offset)
      }

      // Execute query
      const { data, error, count } = await query

      if (error) {
        throw error
      }

      return {
        data,
        count,
        success: true
      }
    } catch (error) {
      logger.error(`Database query error on table ${table}:`, error)
      throw error
    }
  },

  // Insert helper
  async insert(table, data, options = {}) {
    const { returning = '*', onConflict = null } = options

    try {
      let query = supabase.from(table).insert(data)

      if (onConflict) {
        query = query.onConflict(onConflict)
      }

      if (returning !== '*') {
        query = query.select(returning)
      }

      const { data: result, error } = await query

      if (error) {
        throw error
      }

      return {
        data: result,
        success: true
      }
    } catch (error) {
      logger.error(`Database insert error on table ${table}:`, error)
      throw error
    }
  },

  // Update helper
  async update(table, data, where, options = {}) {
    const { returning = '*' } = options

    try {
      let query = supabase.from(table).update(data)

      // Apply filters
      Object.entries(where).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          query = query.in(key, value)
        } else {
          query = query.eq(key, value)
        }
      })

      if (returning !== '*') {
        query = query.select(returning)
      }

      const { data: result, error } = await query

      if (error) {
        throw error
      }

      return {
        data: result,
        success: true
      }
    } catch (error) {
      logger.error(`Database update error on table ${table}:`, error)
      throw error
    }
  },

  // Delete helper
  async delete(table, where, options = {}) {
    const { returning = '*' } = options

    try {
      let query = supabase.from(table).delete()

      // Apply filters
      Object.entries(where).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          query = query.in(key, value)
        } else {
          query = query.eq(key, value)
        }
      })

      if (returning !== '*') {
        query = query.select(returning)
      }

      const { data: result, error } = await query

      if (error) {
        throw error
      }

      return {
        data: result,
        success: true
      }
    } catch (error) {
      logger.error(`Database delete error on table ${table}:`, error)
      throw error
    }
  },

  // Get single record
  async findOne(table, where, options = {}) {
    const { select = '*' } = options

    try {
      let query = supabase.from(table).select(select)

      // Apply filters
      Object.entries(where).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          query = query.in(key, value)
        } else {
          query = query.eq(key, value)
        }
      })

      query = query.single()

      const { data, error } = await query

      if (error) {
        if (error.code === 'PGRST116') {
          // No rows returned
          return { data: null, success: true }
        }
        throw error
      }

      return {
        data,
        success: true
      }
    } catch (error) {
      logger.error(`Database findOne error on table ${table}:`, error)
      throw error
    }
  },

  // Count records
  async count(table, where = {}) {
    try {
      let query = supabase.from(table).select('*', { count: 'exact', head: true })

      // Apply filters
      Object.entries(where).forEach(([key, value]) => {
        if (Array.isArray(value)) {
          query = query.in(key, value)
        } else {
          query = query.eq(key, value)
        }
      })

      const { count, error } = await query

      if (error) {
        throw error
      }

      return {
        count,
        success: true
      }
    } catch (error) {
      logger.error(`Database count error on table ${table}:`, error)
      throw error
    }
  }
}

// Transaction helper (for multiple operations)
const transaction = async (operations) => {
  try {
    const results = []

    for (const operation of operations) {
      const { type, table, data, where, options } = operation

      let result
      switch (type) {
        case 'insert':
          result = await db.insert(table, data, options)
          break
        case 'update':
          result = await db.update(table, data, where, options)
          break
        case 'delete':
          result = await db.delete(table, where, options)
          break
        default:
          throw new Error(`Unknown operation type: ${type}`)
      }

      results.push(result)
    }

    return {
      results,
      success: true
    }
  } catch (error) {
    logger.error('Transaction error:', error)
    throw error
  }
}

// Initialize database connection
const initializeDatabase = async () => {
  const isConnected = await testConnection()
  
  if (!isConnected) {
    throw new Error('Failed to connect to database')
  }

  logger.info('Database initialized successfully')
}

module.exports = {
  supabase,
  db,
  transaction,
  testConnection,
  initializeDatabase
}
