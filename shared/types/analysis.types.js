/**
 * TypeScript/JSDoc types for Analysis entities
 * Shared between frontend and backend services
 */

/**
 * @typedef {Object} AnalysisRequest
 * @property {string} resumeId - Resume ID to analyze
 * @property {Object} [options] - Analysis options
 * @property {boolean} [options.deepAnalysis=false] - Enable deep analysis
 * @property {boolean} [options.includeSkills=true] - Include skills analysis
 * @property {boolean} [options.includeExperience=true] - Include experience analysis
 * @property {boolean} [options.includeEducation=true] - Include education analysis
 * @property {boolean} [options.includeFormat=true] - Include format analysis
 * @property {boolean} [options.includeSuggestions=true] - Include suggestions
 * @property {string} [options.targetRole] - Target role for analysis
 * @property {string} [options.industry] - Target industry
 * @property {Array<string>} [options.customKeywords] - Custom keywords to emphasize
 * @property {string} [options.language] - Language code (auto-detect if not provided)
 * @property {boolean} [options.generateCoverLetter=false] - Generate cover letter
 * @property {boolean} [options.exportPDF=false] - Generate PDF report
 */

/**
 * @typedef {Object} AnalysisResponse
 * @property {boolean} success - Analysis success status
 * @property {Object} analysis - Complete analysis result
 * @property {string} analysisId - Analysis ID
 * @property {string} message - Success message
 * @property {Object} [metadata] - Analysis metadata
 * @property {number} [metadata.processingTime] - Processing time in ms
 * @property {string} [metadata.version] - Analyzer version
 */

/**
 * @typedef {Object} AnalysisResult
 * @property {string} id - Unique identifier
 * @property {string} resumeId - Reference to resume
 * @property {number} overallScore - Overall score (0-100)
 * @property {Object} scores - Detailed scores
 * @property {number} scores.skills - Skills score (0-100)
 * @property {number} scores.experience - Experience score (0-100)
 * @property {number} scores.education - Education score (0-100)
 * @property {number} scores.format - Format and structure score (0-100)
 * @property {number} scores.readability - Readability score (0-100)
 * @property {number} scores.keywordDensity - Keyword density score (0-100)
 * @property {Object} scoreBreakdown - Score breakdown by category
 * @property {Object} scoreBreakdown.skills - Skills score details
 * @property {Object} scoreBreakdown.experience - Experience score details
 * @property {Object} scoreBreakdown.education - Education score details
 * @property {Object} scoreBreakdown.format - Format score details
 * @property {Array<Skill>} skills - Extracted and analyzed skills
 * @property {Array<Experience>} experience - Parsed experience entries
 * @property {Array<Education>} education - Parsed education entries
 * @property {string} language - Detected language code
 * @property {Object} languageAnalysis - Language analysis details
 * @property {string} languageAnalysis.detectedLanguage - Detected language
 * @property {number} languageAnalysis.confidence - Detection confidence
 * @property {Object} recommendations - Analysis recommendations
 * @property {Array<string>} recommendations.general - General recommendations
 * @property {Array<string>} recommendations.skills - Skills improvements
 * @property {Array<string>} recommendations.experience - Experience improvements
 * @property {Array<string>} recommendations.education - Education improvements
 * @property {Array<string>} recommendations.format - Format improvements
 * @property {Object} strengths - Identified strengths
 * @property {Array<string>} strengths.overall - Overall strengths
 * @property {Array<string>} strengths.skills - Skills strengths
 * @property {Array<string>} strengths.experience - Experience strengths
 * @property {Array<string>} strengths.education - Education strengths
 * @property {Array<string>} strengths.format - Format strengths
 * @property {Array<string>} missingSkills - Suggested missing skills
 * @property {Object} skillGaps - Skill gap analysis
 * @property {Array<string>} skillGaps.technical - Missing technical skills
 * @property {Array<string>} skillGaps.business - Missing business skills
 * @property {Array<string>} skillGaps.softSkills - Missing soft skills
 * @property {Object} formatChecks - Format validation results
 * @property {boolean} formatChecks.appropriateLength - Length check
 * @property {boolean} formatChecks.contactInfo - Contact information check
 * @property {boolean} formatChecks.properStructure - Structure check
 * @property {boolean} formatChecks.grammarSpelling - Grammar and spelling check
 * @property {boolean} formatChecks.keywordUsage - Keyword usage check
 * @property {boolean} formatChecks.bulletPoints - Bullet point usage check
 * @property {Object} industryAnalysis - Industry-specific analysis
 * @property {string} industryAnalysis.detectedIndustry - Detected industry
 * @property {number} industryAnalysis.relevanceScore - Industry relevance score
 * @property {Array<string>} industryAnalysis.industryKeywords - Industry keywords found
 * @property {Array<string>} industryAnalysis.missingKeywords - Missing industry keywords
 * @property {Object} careerProgression - Career progression analysis
 * @property {string} careerProgression.level - Progression level (strong, moderate, weak, stagnant)
 * @property {number} careerProgression.score - Progression score (0-100)
 * @property {Array<string>} careerProgression.indicators - Progression indicators
 * @property {Object} readabilityMetrics - Readability metrics
 * @property {number} readabilityMetrics.avgSentenceLength - Average sentence length
 * @property {number} readabilityMetrics.avgWordLength - Average word length
 * @property {number} readabilityMetrics.readabilityScore - Readability score (0-100)
 * @property {number} readabilityMetrics.sentenceCount - Sentence count
 * @property {number} readabilityMetrics.wordCount - Word count
 * @property {Object} contactInfo - Extracted contact information
 * @property {Array<string>} contactInfo.emails - Email addresses
 * @property {Array<string>} contactInfo.phones - Phone numbers
 * @property {Array<string>} contactInfo.websites - Websites
 * @property {Array<string>} contactInfo.linkedin - LinkedIn profiles
 * @property {Object} metadata - Analysis metadata
 * @property {string} metadata.analysisDate - Analysis timestamp
 * @property {number} metadata.processingTime - Processing time in ms
 * @property {string} metadata.analyzerVersion - Analyzer version
 * @property {string} metadata.language - Analysis language
 * @property {Object} metadata.options - Analysis options used
 * @property {string} createdAt - Creation timestamp
 * @property {string} updatedAt - Last update timestamp
 */

/**
 * @typedef {Object} SkillAnalysis
 * @property {Array<Skill>} extractedSkills - All extracted skills
 * @property {Object} statistics - Skill statistics
 * @property {number} statistics.totalSkills - Total skills found
 * @property {Object} statistics.categories - Skills by category
 * @property {Object} statistics.confidenceDistribution - Confidence distribution
 * @property {Object} statistics.methods - Extraction methods distribution
 * @property {number} statistics.averageConfidence - Average confidence
 * @property {Array<Object>} statistics.topSkills - Top skills by score
 * @property {Array<string>} suggestions - Skill improvement suggestions
 * @property {Array<string>} missingSkills - Missing skills for target role
 * @property {Object} skillMatrix - Skill matrix by category and level
 * @property {number} skillScore - Overall skills score
 */

/**
 * @typedef {Object} ExperienceAnalysis
 * @property {Array<Experience>} parsedExperience - Parsed experience entries
 * @property {Object} summary - Experience summary
 * @property {number} summary.totalPositions - Total positions
 * @property {number} summary.totalExperienceYears - Total years of experience
 * @property {number} summary.currentPositions - Current positions
 * @property {Array<string>} summary.companies - Companies worked at
 * @property {number} summary.companyCount - Number of companies
 * @property {string} summary.careerProgression - Career progression level
 * @property {number} summary.averagePositionDuration - Average position duration
 * @property {Object} metrics - Experience metrics
 * @property {number} metrics.totalAchievements - Total achievements
 * @property {number} metrics.quantifiableAchievements - Quantifiable achievements
 * @property {number} metrics.actionVerbUsage - Action verb usage score
 * @property {number} metrics.technicalKeywordCount - Technical keyword count
 * @property {number} metrics.managementKeywordCount - Management keyword count
 * @property {Array<string>} suggestions - Experience improvement suggestions
 * @property {number} experienceScore - Overall experience score
 */

/**
 * @typedef {Object} EducationAnalysis
 * @property {Array<Education>} parsedEducation - Parsed education entries
 * @property {Object} summary - Education summary
 * @property {number} summary.totalEducation - Total education entries
 * @property {string} summary.highestLevel - Highest education level
 * @property {number} summary.highestLevelScore - Highest level score
 * @property {Array<string>} summary.institutions - Institutions attended
 * @property {number} summary.institutionCount - Number of institutions
 * @property {Array<string>} summary.fields - Fields of study
 * @property {number} summary.fieldCount - Number of fields
 * @property {boolean} summary.hasGPA - Has GPA information
 * @property {number} summary.averageGPA - Average GPA
 * @property {number} summary.achievementsCount - Total achievements
 * @property {Object} relevance - Education relevance analysis
 * @property {number} relevance.relevanceScore - Relevance score (0-100)
 * @property {Array<string>} relevance.relevantDegrees - Relevant degrees
 * @property {boolean} relevance.fieldMatch - Field match status
 * @property {Array<string>} relevance.recommendations - Relevance recommendations
 * @property {number} educationScore - Overall education score
 */

/**
 * @typedef {Object} FormatAnalysis
 * @property {Object} structure - Structure analysis
 * @property {Array<string>} structure.foundSections - Found sections
 * @property {Array<string>} structure.missingSections - Missing sections
 * @property {number} structure.structureScore - Structure score (0-100)
 * @property {Object} formatting - Formatting analysis
 * @property {number} formatting.bulletPointUsage - Bullet point usage
 * @property {number} formatting.whiteSpaceUsage - White space usage
 * @property {number} formatting.consistencyScore - Consistency score
 * @property {Object} content - Content analysis
 * @property {number} content.actionVerbDensity - Action verb density
 * @property {number} content.quantifiableContent - Quantifiable content
 * @property {number} content.keywordDensity - Keyword density
 * @property {Object} contact - Contact information analysis
 * @property {boolean} contact.hasEmail - Has email
 * @property {boolean} contact.hasPhone - Has phone
 * @property {boolean} contact.hasLinkedIn - Has LinkedIn
 * @property {number} contact.completenessScore - Contact completeness score
 * @property {Array<string>} recommendations - Format improvement suggestions
 * @property {number} formatScore - Overall format score
 */

/**
 * @typedef {Object} CoverLetterRequest
 * @property {string} resumeId - Resume ID
 * @property {string} jobDescription - Job description text
 * @property {string} [companyName] - Company name
 * @property {string} [hiringManager] - Hiring manager name
 * @property {string} [language] - Language code
 * @property {Object} [options] - Generation options
 * @property {string} [options.tone] - Tone (professional, casual, enthusiastic)
 * @property {number} [options.length] - Length (short, medium, long)
 * @property {boolean} [options.includeAchievements=true] - Include achievements
 * @property {boolean} [options.customizeForJob=true] - Customize for job
 */

/**
 * @typedef {Object} CoverLetterResponse
 * @property {boolean} success - Generation success status
 * @property {string} coverLetter - Generated cover letter
 * @property {Object} metadata - Generation metadata
 * @property {string} metadata.generatedAt - Generation timestamp
 * @property {string} metadata.wordCount - Word count
 * @property {string} [message] - Success message
 */

/**
 * @typedef {Object} ComparisonRequest
 * @property {string} resumeId1 - First resume ID
 * @property {string} resumeId2 - Second resume ID
 * @property {Object} [options] - Comparison options
 * @property {boolean} [options.includeSkills=true] - Include skills comparison
 * @property {boolean} [options.includeExperience=true] - Include experience comparison
 * @property {boolean} [options.includeEducation=true] - Include education comparison
 * @property {boolean} [options.includeScores=true] - Include score comparison
 */

/**
 * @typedef {Object} ComparisonResponse
 * @property {boolean} success - Comparison success status
 * @property {Object} comparison - Comparison results
 * @property {Object} comparison.scores - Score comparison
 * @property {Object} comparison.skills - Skills comparison
 * @property {Object} comparison.experience - Experience comparison
 * @property {Object} comparison.education - Education comparison
 * @property {Object} comparison.summary - Comparison summary
 * @property {string} [message] - Success message
 */

/**
 * @typedef {Object} BulkAnalysisRequest
 * @property {Array<string>} resumeIds - Resume IDs to analyze
 * @property {Object} [options] - Analysis options (applied to all)
 * @property {boolean} [options.parallel=true] - Process in parallel
 * @property {number} [options.maxConcurrency=5] - Max concurrent analyses
 */

/**
 * @typedef {Object} BulkAnalysisResponse
 * @property {boolean} success - Bulk analysis success status
 * @property {Array<Object>} results - Analysis results
 * @property {Object} summary - Bulk analysis summary
 * @property {number} summary.total - Total resumes
 * @property {number} summary.successful - Successful analyses
 * @property {number} summary.failed - Failed analyses
 * @property {number} summary.averageScore - Average score
 * @property {string} [message] - Success message
 */

/**
 * @typedef {Object} AnalysisExportRequest
 * @property {string} analysisId - Analysis ID to export
 * @property {string} format - Export format (pdf, docx, json)
 * @property {Object} [options] - Export options
 * @property {boolean} [options.includeDetails=true] - Include detailed analysis
 * @property {boolean} [options.includeCharts=true] - Include charts
 * @property {boolean} [options.includeRecommendations=true] - Include recommendations
 */

/**
 * @typedef {Object} AnalysisExportResponse
 * @property {boolean} success - Export success status
 * @property {string} downloadUrl - Download URL
 * @property {string} filename - Generated filename
 * @property {number} fileSize - File size in bytes
 * @property {string} expiresAt - Download URL expiration
 * @property {string} [message] - Success message
 */

/**
 * @typedef {Object} AnalysisHistoryRequest
 * @property {string} [resumeId] - Filter by resume ID
 * @property {string} [userId] - Filter by user ID
 * @property {string} [dateFrom] - Filter by date from
 * @property {string} [dateTo] - Filter by date to
 * @property {number} [page=1] - Page number
 * @property {number} [limit=20] - Items per page
 * @property {string} [sort=createdAt] - Sort field
 * @property {string} [order=desc] - Sort order
 */

/**
 * @typedef {Object} AnalysisHistoryResponse
 * @property {boolean} success - Request success status
 * @property {Array<Object>} analyses - Analysis history
 * @property {Object} pagination - Pagination info
 * @property {Object} statistics - Statistics
 * @property {string} [message] - Success message
 */

/**
 * @typedef {Object} AnalysisStatistics
 * @property {number} totalAnalyses - Total analyses performed
 * @property {number} averageScore - Average score across all analyses
 * @property {number} averageProcessingTime - Average processing time
 * @property {Object} scoreDistribution - Score distribution
 * @property {Object} languageDistribution - Language distribution
 * @property {Object} industryDistribution - Industry distribution
 * @property {Array<string}> mostCommonSkills - Most common skills
 * @property {Array<string}> mostCommonIssues - Most common issues
 * @property {Object} trends - Analysis trends over time
 */

// Export types for ES6 modules
export {
  AnalysisRequest,
  AnalysisResponse,
  AnalysisResult,
  SkillAnalysis,
  ExperienceAnalysis,
  EducationAnalysis,
  FormatAnalysis,
  CoverLetterRequest,
  CoverLetterResponse,
  ComparisonRequest,
  ComparisonResponse,
  BulkAnalysisRequest,
  BulkAnalysisResponse,
  AnalysisExportRequest,
  AnalysisExportResponse,
  AnalysisHistoryRequest,
  AnalysisHistoryResponse,
  AnalysisStatistics
}

// For CommonJS environments
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    AnalysisRequest,
    AnalysisResponse,
    AnalysisResult,
    SkillAnalysis,
    ExperienceAnalysis,
    EducationAnalysis,
    FormatAnalysis,
    CoverLetterRequest,
    CoverLetterResponse,
    ComparisonRequest,
    ComparisonResponse,
    BulkAnalysisRequest,
    BulkAnalysisResponse,
    AnalysisExportRequest,
    AnalysisExportResponse,
    AnalysisHistoryRequest,
    AnalysisHistoryResponse,
    AnalysisStatistics
  }
}
