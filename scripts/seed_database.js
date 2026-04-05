#!/usr/bin/env node

/**
 * Database seeding script for AI CV Optimizer
 * Creates sample data for development and testing
 */

const { createClient } = require('@supabase/supabase-js')
const { v4: uuidv4 } = require('uuid')
require('dotenv').config()

// Configuration
const supabaseUrl = process.env.SUPABASE_URL
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY

if (!supabaseUrl || !supabaseServiceKey) {
  console.error('Missing Supabase configuration. Please check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables.')
  process.exit(1)
}

const supabase = createClient(supabaseUrl, supabaseServiceKey)

// Sample data
const sampleUsers = [
  {
    id: uuidv4(),
    email: 'john.doe@example.com',
    first_name: 'John',
    last_name: 'Doe',
    clerk_id: 'user_123456789',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: uuidv4(),
    email: 'jane.smith@example.com',
    first_name: 'Jane',
    last_name: 'Smith',
    clerk_id: 'user_987654321',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
]

const sampleResumes = [
  {
    id: uuidv4(),
    user_id: sampleUsers[0].id,
    original_name: 'john_doe_resume.pdf',
    file_name: `resume_${uuidv4()}.pdf`,
    mime_type: 'application/pdf',
    file_size: 524288,
    status: 'completed',
    extracted_text: `John Doe
Senior Software Engineer

Experience:
Senior Software Engineer at Tech Corp (2020-Present)
- Led development of microservices architecture
- Improved system performance by 40%
- Managed team of 5 developers

Software Engineer at StartupXYZ (2018-2020)
- Developed RESTful APIs
- Implemented CI/CD pipelines
- Reduced deployment time by 60%

Education:
Bachelor of Science in Computer Science
University of Technology (2014-2018)

Skills:
JavaScript, Python, React, Node.js, AWS, Docker, Kubernetes`,
    metadata: {
      upload_date: new Date().toISOString(),
      processing_date: new Date().toISOString(),
      text_length: 2500,
      word_count: 400,
      language: 'en'
    },
    is_public: false,
    target_job: 'Senior Software Engineer',
    industry: 'Technology',
    tags: ['software', 'engineering', 'javascript', 'python'],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: uuidv4(),
    user_id: sampleUsers[1].id,
    original_name: 'jane_smith_resume.pdf',
    file_name: `resume_${uuidv4()}.pdf`,
    mime_type: 'application/pdf',
    file_size: 471859,
    status: 'completed',
    extracted_text: `Jane Smith
Product Manager

Experience:
Senior Product Manager at ProductCo (2019-Present)
- Launched 3 successful products
- Increased user engagement by 35%
- Managed cross-functional teams

Product Manager at TechStart (2017-2019)
- Conducted market research
- Defined product roadmap
- Collaborated with engineering teams

Education:
MBA from Business School (2015-2017)
Bachelor of Arts in Marketing (2011-2015)

Skills:
Product Management, Market Research, Analytics, Agile, Scrum, User Research`,
    metadata: {
      upload_date: new Date().toISOString(),
      processing_date: new Date().toISOString(),
      text_length: 2200,
      word_count: 350,
      language: 'en'
    },
    is_public: true,
    target_job: 'Senior Product Manager',
    industry: 'Technology',
    tags: ['product', 'management', 'agile', 'scrum'],
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
]

const sampleAnalyses = [
  {
    id: uuidv4(),
    resume_id: sampleResumes[0].id,
    overall_score: 85,
    scores: {
      skills: 88,
      experience: 82,
      education: 90,
      format: 85
    },
    skills: [
      {
        name: 'JavaScript',
        category: 'technical',
        subcategory: 'programming',
        confidence: 0.95,
        method: 'keyword',
        count: 3,
        context: 'JavaScript, React, Node.js',
        tfidf_score: 0.85,
        final_score: 0.92
      },
      {
        name: 'Python',
        category: 'technical',
        subcategory: 'programming',
        confidence: 0.90,
        method: 'keyword',
        count: 2,
        context: 'Python, Django',
        tfidf_score: 0.78,
        final_score: 0.86
      }
    ],
    experience: [
      {
        title: 'Senior Software Engineer',
        company: 'Tech Corp',
        location: 'San Francisco, CA',
        start_date: '2020',
        end_date: 'Present',
        duration_years: 4,
        description: 'Led development of microservices architecture',
        achievements: ['Improved system performance by 40%', 'Managed team of 5 developers'],
        metrics: {
          quantifiable_achievements: 2,
          action_verb_count: 3,
          technical_keywords: 5,
          management_keywords: 2,
          achievement_count: 2,
          description_length: 50,
          has_metrics: true
        },
        is_current: true,
        confidence: 0.92
      }
    ],
    education: [
      {
        degree: 'Bachelor of Science',
        field: 'Computer Science',
        institution: 'University of Technology',
        location: 'Boston, MA',
        start_date: '2014',
        end_date: '2018',
        gpa: 3.8,
        achievements: ['Dean\'s List', 'Graduated Magna Cum Laude'],
        level_score: 3,
        is_current: false,
        confidence: 0.95
      }
    ],
    language: 'en',
    language_analysis: {
      detected_language: 'en',
      confidence: 0.98
    },
    recommendations: {
      general: [
        'Add more quantifiable achievements to your experience section',
        'Consider including a professional summary at the top'
      ],
      skills: [
        'Highlight more cloud technologies you\'ve worked with',
        'Add more specific framework experience'
      ],
      format: [
        'Use bullet points consistently throughout',
        'Consider adding a skills section with proficiency levels'
      ]
    },
    strengths: {
      overall: [
        'Strong technical background',
        'Clear career progression',
        'Good educational foundation'
      ],
      skills: [
        'Strong programming skills',
        'Good variety of technologies'
      ]
    },
    missing_skills: [
      'GraphQL',
      'TypeScript',
      'AWS Lambda'
    ],
    format_checks: {
      appropriate_length: true,
      contact_info: true,
      proper_structure: true,
      grammar_spelling: true,
      keyword_usage: true,
      bullet_points: true
    },
    metadata: {
      analysis_date: new Date().toISOString(),
      processing_time: 2500,
      analyzer_version: '1.2.0',
      language: 'en'
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: uuidv4(),
    resume_id: sampleResumes[1].id,
    overall_score: 78,
    scores: {
      skills: 75,
      experience: 80,
      education: 85,
      format: 72
    },
    skills: [
      {
        name: 'Product Management',
        category: 'business',
        subcategory: 'management',
        confidence: 0.92,
        method: 'keyword',
        count: 4,
        context: 'Product Manager, Senior Product Manager',
        tfidf_score: 0.88,
        final_score: 0.90
      }
    ],
    experience: [
      {
        title: 'Senior Product Manager',
        company: 'ProductCo',
        location: 'New York, NY',
        start_date: '2019',
        end_date: 'Present',
        duration_years: 5,
        description: 'Launched 3 successful products',
        achievements: ['Increased user engagement by 35%', 'Managed cross-functional teams'],
        metrics: {
          quantifiable_achievements: 2,
          action_verb_count: 3,
          technical_keywords: 1,
          management_keywords: 4,
          achievement_count: 2,
          description_length: 35,
          has_metrics: true
        },
        is_current: true,
        confidence: 0.88
      }
    ],
    education: [
      {
        degree: 'MBA',
        field: 'Business Administration',
        institution: 'Business School',
        location: 'Chicago, IL',
        start_date: '2015',
        end_date: '2017',
        gpa: 3.6,
        achievements: ['Beta Gamma Sigma'],
        level_score: 4.5,
        is_current: false,
        confidence: 0.90
      }
    ],
    language: 'en',
    language_analysis: {
      detected_language: 'en',
      confidence: 0.96
    },
    recommendations: {
      general: [
        'Add more specific metrics to your achievements',
        'Include a professional summary section'
      ],
      format: [
        'Improve formatting consistency',
        'Add more white space for readability'
      ]
    },
    strengths: {
      overall: [
        'Strong business background',
        'Clear career progression',
        'Good educational credentials'
      ]
    },
    missing_skills: [
      'Data Analysis',
      'SQL',
      'Tableau'
    ],
    format_checks: {
      appropriate_length: true,
      contact_info: true,
      proper_structure: true,
      grammar_spelling: true,
      keyword_usage: false,
      bullet_points: false
    },
    metadata: {
      analysis_date: new Date().toISOString(),
      processing_time: 2200,
      analyzer_version: '1.2.0',
      language: 'en'
    },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
]

// Seeding functions
async function seedDatabase() {
  console.log('🌱 Starting database seeding...')
  
  try {
    // Create profiles (users)
    console.log('📝 Creating user profiles...')
    for (const user of sampleUsers) {
      const { error } = await supabase
        .from('profiles')
        .insert(user)
      
      if (error) {
        console.error(`❌ Error creating user ${user.email}:`, error)
      } else {
        console.log(`✅ Created user: ${user.email}`)
      }
    }

    // Create resumes
    console.log('📄 Creating resumes...')
    for (const resume of sampleResumes) {
      const { error } = await supabase
        .from('resumes')
        .insert(resume)
      
      if (error) {
        console.error(`❌ Error creating resume ${resume.original_name}:`, error)
      } else {
        console.log(`✅ Created resume: ${resume.original_name}`)
      }
    }

    // Create analyses
    console.log('🔍 Creating analyses...')
    for (const analysis of sampleAnalyses) {
      const { error } = await supabase
        .from('analyses')
        .insert(analysis)
      
      if (error) {
        console.error(`❌ Error creating analysis for resume ${analysis.resume_id}:`, error)
      } else {
        console.log(`✅ Created analysis with score: ${analysis.overall_score}`)
      }
    }

    console.log('🎉 Database seeding completed successfully!')
    
  } catch (error) {
    console.error('❌ Error during seeding:', error)
    process.exit(1)
  }
}

// Clean database
async function cleanDatabase() {
  console.log('🧹 Cleaning database...')
  
  try {
    // Delete in reverse order of dependencies
    const { error: analysesError } = await supabase
      .from('analyses')
      .delete()
      .neq('id', '00000000-0000-0000-0000-000000000000')
    
    if (analysesError) {
      console.error('❌ Error deleting analyses:', analysesError)
    } else {
      console.log('✅ Deleted all analyses')
    }

    const { error: resumesError } = await supabase
      .from('resumes')
      .delete()
      .neq('id', '00000000-0000-0000-0000-000000000000')
    
    if (resumesError) {
      console.error('❌ Error deleting resumes:', resumesError)
    } else {
      console.log('✅ Deleted all resumes')
    }

    const { error: profilesError } = await supabase
      .from('profiles')
      .delete()
      .neq('id', '00000000-0000-0000-0000-000000000000')
    
    if (profilesError) {
      console.error('❌ Error deleting profiles:', profilesError)
    } else {
      console.log('✅ Deleted all profiles')
    }

    console.log('🧹 Database cleaning completed!')
    
  } catch (error) {
    console.error('❌ Error during cleaning:', error)
    process.exit(1)
  }
}

// Command line interface
const command = process.argv[2]

if (command === 'seed') {
  seedDatabase()
} else if (command === 'clean') {
  cleanDatabase()
} else if (command === 'reset') {
  cleanDatabase().then(() => {
    setTimeout(seedDatabase, 2000)
  })
} else {
  console.log('Usage: node seed_database.js [seed|clean|reset]')
  console.log('  seed  - Insert sample data')
  console.log('  clean - Delete all sample data')
  console.log('  reset - Clean and then seed')
  process.exit(1)
}
