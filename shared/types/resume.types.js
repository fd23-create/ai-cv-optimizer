/**
 * TypeScript/JSDoc types for Resume entities
 * Shared between frontend and backend services
 */

/**
 * @typedef {Object} Resume
 * @property {string} id - Unique identifier
 * @property {string} userId - Owner user ID
 * @property {string} originalName - Original filename
 * @property {string} fileName - Stored filename
 * @property {string} mimeType - File MIME type
 * @property {number} fileSize - File size in bytes
 * @property {string} status - Processing status (pending, processing, completed, failed)
 * @property {string} extractedText - Extracted text content
 * @property {Object} metadata - File metadata
 * @property {string} metadata.uploadDate - Upload timestamp
 * @property {string} metadata.processingDate - Processing completion timestamp
 * @property {number} metadata.textLength - Length of extracted text
 * @property {number} metadata.wordCount - Word count
 * @property {string} metadata.language - Detected language
 * @property {string} createdAt - Creation timestamp
 * @property {string} updatedAt - Last update timestamp
 * @property {string|null} analysisId - Reference to analysis result
 * @property {Object|null} analysis - Analysis result (embedded)
 * @property {boolean} isPublic - Whether resume is publicly accessible
 * @property {string|null} targetJob - Target job/position
 * @property {string|null} industry - Target industry
 * @property {Array<string>} tags - User-defined tags
 */

/**
 * @typedef {Object} ResumeAnalysis
 * @property {string} id - Unique identifier
 * @property {string} resumeId - Reference to resume
 * @property {number} overallScore - Overall score (0-100)
 * @property {Object} scores - Component scores
 * @property {number} scores.skills - Skills score (0-100)
 * @property {number} scores.experience - Experience score (0-100)
 * @property {number} scores.education - Education score (0-100)
 * @property {number} scores.format - Format score (0-100)
 * @property {Array<Object>} skills - Extracted skills
 * @property {Array<Object>} experience - Extracted experience
 * @property {Array<Object>} education - Extracted education
 * @property {string} language - Detected language
 * @property {Array<string>} recommendations - General recommendations
 * @property {Array<string>} strengths - Identified strengths
 * @property {Array<string>} improvements - Areas for improvement
 * @property {Array<string>} missingSkills - Suggested missing skills
 * @property {Object} formatChecks - Format validation results
 * @property {boolean} formatChecks.length - Appropriate length check
 * @property {boolean} formatChecks.contact - Contact info check
 * @property {boolean} formatChecks.structure - Structure check
 * @property {boolean} formatChecks.grammar - Grammar check
 * @property {boolean} formatChecks.keywords - Keywords check
 * @property {Object} metadata - Analysis metadata
 * @property {string} metadata.analysisDate - Analysis timestamp
 * @property {number} metadata.processingTime - Processing time in ms
 * @property {string} metadata.analyzerVersion - Analyzer version
 * @property {string} createdAt - Creation timestamp
 * @property {string} updatedAt - Last update timestamp
 */

/**
 * @typedef {Object} Skill
 * @property {string} name - Skill name
 * @property {string} category - Skill category (technical, business, soft_skills, tools)
 * @property {string} subcategory - Skill subcategory
 * @property {number} confidence - Confidence score (0-1)
 * @property {string} method - Extraction method (keyword, pattern, entity, yake)
 * @property {number} count - Occurrence count
 * @property {string} context - Context snippet
 * @property {number} tfidfScore - TF-IDF score
 * @property {number} finalScore - Final relevance score
 * @property {Array<string>} methods - All extraction methods used
 */

/**
 * @typedef {Object} Experience
 * @property {string} title - Position title
 * @property {string} company - Company name
 * @property {string} location - Location
 * @property {string|null} startDate - Start date
 * @property {string|null} endDate - End date
 * @property {number} durationYears - Duration in years
 * @property {string} description - Position description
 * @property {Array<string>} achievements - Achievement list
 * @property {Object} metrics - Position metrics
 * @property {number} metrics.quantifiableAchievements - Number of quantifiable achievements
 * @property {number} metrics.actionVerbCount - Action verb count
 * @property {number} metrics.technicalKeywords - Technical keyword count
 * @property {number} metrics.managementKeywords - Management keyword count
 * @property {number} metrics.achievementCount - Total achievement count
 * @property {number} metrics.descriptionLength - Description length
 * @property {boolean} metrics.hasMetrics - Has quantifiable metrics
 * @property {boolean} isCurrent - Whether this is current position
 * @property {number} confidence - Parsing confidence (0-1)
 */

/**
 * @typedef {Object} Education
 * @property {string} degree - Degree name
 * @property {string} field - Field of study
 * @property {string} institution - Institution name
 * @property {string} location - Location
 * @property {string|null} startDate - Start date
 * @property {string|null} endDate - End date
 * @property {number|null} gpa - GPA score
 * @property {Array<string>} achievements - Achievements and honors
 * @property {number} levelScore - Education level score
 * @property {boolean} isCurrent - Whether currently studying
 * @property {number} confidence - Parsing confidence (0-1)
 */

/**
 * @typedef {Object} ResumeUploadRequest
 * @property {File} file - Resume file
 * @property {string} [title] - Optional title
 * @property {string} [description] - Optional description
 * @property {string} [targetJob] - Target job/position
 * @property {string} [industry] - Target industry
 * @property {Object} [options] - Analysis options
 * @property {boolean} [options.includeSkills=true] - Include skills analysis
 * @property {boolean} [options.includeExperience=true] - Include experience analysis
 * @property {boolean} [options.includeEducation=true] - Include education analysis
 * @property {boolean} [options.includeFormat=true] - Include format analysis
 * @property {Array<string>} [options.customKeywords] - Custom keywords to look for
 */

/**
 * @typedef {Object} ResumeUploadResponse
 * @property {boolean} success - Upload success status
 * @property {Object} resume - Created resume object
 * @property {string} message - Success message
 * @property {Object} [analysis] - Analysis result if completed immediately
 */

/**
 * @typedef {Object} AnalysisRequest
 * @property {string} resumeId - Resume ID to analyze
 * @property {Object} [options] - Analysis options
 * @property {boolean} [options.includeSkills=true] - Include skills analysis
 * @property {boolean} [options.includeExperience=true] - Include experience analysis
 * @property {boolean} [options.includeEducation=true] - Include education analysis
 * @property {boolean} [options.includeFormat=true] - Include format analysis
 * @property {Array<string>} [options.customKeywords] - Custom keywords
 */

/**
 * @typedef {Object} AnalysisResponse
 * @property {boolean} success - Analysis success status
 * @property {Object} analysis - Analysis result
 * @property {string} message - Success message
 */

/**
 * @typedef {Object} ResumeListRequest
 * @property {number} [page=1] - Page number
 * @property {number} [limit=20] - Items per page
 * @property {string} [sort=createdAt] - Sort field
 * @property {string} [order=desc] - Sort order (asc/desc)
 * @property {string} [status] - Filter by status
 * @property {number} [minScore] - Filter by minimum score
 * @property {number} [maxScore] - Filter by maximum score
 * @property {string} [industry] - Filter by industry
 * @property {string} [dateFrom] - Filter by date from
 * @property {string} [dateTo] - Filter by date to
 */

/**
 * @typedef {Object} ResumeListResponse
 * @property {boolean} success - Request success status
 * @property {Array<Resume>} resumes - Resume list
 * @property {Object} pagination - Pagination info
 * @property {number} pagination.page - Current page
 * @property {number} pagination.limit - Items per page
 * @property {number} pagination.total - Total items
 * @property {number} pagination.pages - Total pages
 * @property {Object} summary - Summary statistics
 * @property {number} summary.totalResumes - Total resumes
 * @property {number} summary.averageScore - Average score
 * @property {number} summary.thisMonth - Resumes this month
 * @property {number} summary.bestScore - Best score
 */

/**
 * @typedef {Object} ResumeUpdateRequest
 * @property {string} [title] - Updated title
 * @property {string} [description] - Updated description
 * @property {string} [targetJob] - Updated target job
 * @property {string} [industry] - Updated industry
 * @property {boolean} [isPublic] - Updated visibility
 * @property {Array<string>} [tags] - Updated tags
 */

/**
 * @typedef {Object} ResumeUpdateResponse
 * @property {boolean} success - Update success status
 * @property {Object} resume - Updated resume object
 * @property {string} message - Success message
 */

/**
 * @typedef {Object} ResumeDeleteResponse
 * @property {boolean} success - Delete success status
 * @property {string} message - Success message
 */

/**
 * @typedef {Object} ValidationError
 * @property {string} field - Field name
 * @property {string} message - Error message
 * @property {*} value - Invalid value
 */

/**
 * @typedef {Object} ApiResponse
 * @property {boolean} success - Request success status
 * @property {*} data - Response data
 * @property {string} [message] - Response message
 * @property {string} [error] - Error message
 * @property {Array<ValidationError>} [details] - Validation error details
 * @property {string} [timestamp] - Response timestamp
 * @property {string} [path] - Request path
 */

/**
 * @typedef {Object} FileValidationResult
 * @property {boolean} valid - Validation status
 * @property {string} message - Validation message
 * @property {string} [errorCode] - Error code
 * @property {number} [fileSize] - File size
 * @property {string} [fileExtension] - File extension
 * @property {string} [mimeType] - MIME type
 */

/**
 * @typedef {Object} TextValidationResult
 * @property {boolean} valid - Validation status
 * @property {string} message - Validation message
 * @property {string} [errorCode] - Error code
 * @property {number} [textLength] - Text length
 * @property {number} [wordCount] - Word count
 * @property {boolean} [hasMeaningfulContent] - Has meaningful content
 */

/**
 * @typedef {Object} StructureValidationResult
 * @property {boolean} valid - Validation status
 * @property {number} structureScore - Structure score (0-100)
 * @property {Array<string>} foundSections - Found sections
 * @property {Array<string>} missingSections - Missing sections
 * @property {Array<string>} issues - Validation issues
 * @property {boolean} hasContactInfo - Has contact information
 * @property {number} dateCount - Date count
 * @property {number} wordCount - Word count
 */

/**
 * @typedef {Object} ValidationSummary
 * @property {boolean} valid - Overall validation status
 * @property {number} overallScore - Overall score
 * @property {Array<string>} issues - All issues
 * @property {Object} fileInfo - File information
 * @property {Object} textInfo - Text information
 * @property {Object} structureInfo - Structure information
 */

// Export types for ES6 modules
export {
  Resume,
  ResumeAnalysis,
  Skill,
  Experience,
  Education,
  ResumeUploadRequest,
  ResumeUploadResponse,
  AnalysisRequest,
  AnalysisResponse,
  ResumeListRequest,
  ResumeListResponse,
  ResumeUpdateRequest,
  ResumeUpdateResponse,
  ResumeDeleteResponse,
  ValidationError,
  ApiResponse,
  FileValidationResult,
  TextValidationResult,
  StructureValidationResult,
  ValidationSummary
}

// For CommonJS environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    Resume,
    ResumeAnalysis,
    Skill,
    Experience,
    Education,
    ResumeUploadRequest,
    ResumeUploadResponse,
    AnalysisRequest,
    AnalysisResponse,
    ResumeListRequest,
    ResumeListResponse,
    ResumeUpdateRequest,
    ResumeUpdateResponse,
    ResumeDeleteResponse,
    ValidationError,
    ApiResponse,
    FileValidationResult,
    TextValidationResult,
    StructureValidationResult,
    ValidationSummary
  }
}
