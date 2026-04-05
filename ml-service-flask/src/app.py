from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import analyzers and utilities
from src.utils.parser import PDFParser
from src.utils.cleaner import TextCleaner
from src.utils.validators import ResumeValidator
from src.analyzers.scorer import ResumeScorer
from src.analyzers.skills_extractor import SkillsExtractor
from src.analyzers.experience_parser import ExperienceParser
from src.analyzers.education_parser import EducationParser
from src.generators.cover_letter import CoverLetterGenerator
from src.generators.suggestions import SuggestionsGenerator
from src.config import Config

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config.from_object(Config)

# Initialize extensions
CORS(app, 
     origins=['http://localhost:3000', 'http://localhost:5000'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limit=os.getenv('RATE_LIMIT', '100/hour')
)

# Setup logging
if not app.debug:
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = RotatingFileHandler(
        'logs/ml_service.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('ML Service startup')

# Initialize components
parser = PDFParser()
cleaner = TextCleaner()
validator = ResumeValidator()
scorer = ResumeScorer()
skills_extractor = SkillsExtractor()
experience_parser = ExperienceParser()
education_parser = EducationParser()
cover_letter_generator = CoverLetterGenerator()
suggestions_generator = SuggestionsGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI CV Optimizer ML Service',
        'version': '1.0.0'
    })

@app.route('/analyze', methods=['POST'])
@limiter.limit('10/minute')
def analyze_resume():
    """Main resume analysis endpoint"""
    try:
        app.logger.info('Starting resume analysis')
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'message': 'Please upload a resume file'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select a file to upload'
            }), 400
        
        # Get options from request
        options = request.form.get('options', '{}')
        try:
            import json
            options = json.loads(options)
        except json.JSONDecodeError:
            options = {}
        
        # Validate file
        validation_result = validator.validate_file(file)
        if not validation_result['valid']:
            return jsonify({
                'error': 'Invalid file',
                'message': validation_result['message']
            }), 400
        
        # Parse PDF
        app.logger.info('Parsing PDF file')
        text_content = parser.extract_text(file)
        if not text_content:
            return jsonify({
                'error': 'Parsing failed',
                'message': 'Could not extract text from the PDF'
            }), 400
        
        # Clean text
        app.logger.info('Cleaning extracted text')
        cleaned_text = cleaner.clean_text(text_content)
        
        # Detect language
        language = cleaner.detect_language(cleaned_text)
        app.logger.info(f'Detected language: {language}')
        
        # Extract sections
        app.logger.info('Extracting resume sections')
        
        # Extract skills
        skills = skills_extractor.extract_skills(cleaned_text, language)
        
        # Extract experience
        experience = experience_parser.extract_experience(cleaned_text, language)
        
        # Extract education
        education = education_parser.extract_education(cleaned_text, language)
        
        # Calculate scores
        app.logger.info('Calculating scores')
        scores = scorer.calculate_scores(
            cleaned_text,
            skills,
            experience,
            education,
            language
        )
        
        # Generate suggestions
        app.logger.info('Generating suggestions')
        suggestions = suggestions_generator.generate_suggestions(
            cleaned_text,
            skills,
            experience,
            education,
            scores,
            language
        )
        
        # Compile analysis result
        analysis_result = {
            'success': True,
            'analysis': {
                'overallScore': scores['overall'],
                'scores': scores,
                'skills': skills,
                'experience': experience,
                'education': education,
                'language': language,
                'recommendations': suggestions['recommendations'],
                'strengths': suggestions['strengths'],
                'improvements': suggestions['improvements'],
                'missingSkills': suggestions['missing_skills'],
                'formatChecks': suggestions['format_checks'],
                'metadata': {
                    'fileSize': len(file.read()) if hasattr(file, 'read') else 0,
                    'textLength': len(cleaned_text),
                    'wordCount': len(cleaned_text.split()),
                    'processingTime': None  # Would be calculated in production
                }
            }
        }
        
        app.logger.info('Resume analysis completed successfully')
        return jsonify(analysis_result)
        
    except Exception as e:
        app.logger.error(f'Error during resume analysis: {str(e)}')
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500

@app.route('/generate-cover-letter', methods=['POST'])
@limiter.limit('5/minute')
def generate_cover_letter():
    """Generate cover letter based on resume and job description"""
    try:
        app.logger.info('Starting cover letter generation')
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Please provide resume text and job description'
            }), 400
        
        resume_text = data.get('resumeText', '')
        job_description = data.get('jobDescription', '')
        language = data.get('language', 'en')
        
        if not resume_text or not job_description:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Both resumeText and jobDescription are required'
            }), 400
        
        # Generate cover letter
        cover_letter = cover_letter_generator.generate(
            resume_text,
            job_description,
            language
        )
        
        app.logger.info('Cover letter generated successfully')
        return jsonify({
            'success': True,
            'coverLetter': cover_letter
        })
        
    except Exception as e:
        app.logger.error(f'Error generating cover letter: {str(e)}')
        return jsonify({
            'error': 'Generation failed',
            'message': str(e)
        }), 500

@app.route('/extract-skills', methods=['POST'])
@limiter.limit('20/minute')
def extract_skills_only():
    """Extract skills from text only"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'message': 'Please provide text to analyze'
            }), 400
        
        text = data['text']
        language = data.get('language', 'en')
        
        skills = skills_extractor.extract_skills(text, language)
        
        return jsonify({
            'success': True,
            'skills': skills
        })
        
    except Exception as e:
        app.logger.error(f'Error extracting skills: {str(e)}')
        return jsonify({
            'error': 'Extraction failed',
            'message': str(e)
        }), 500

@app.route('/score-resume', methods=['POST'])
@limiter.limit('15/minute')
def score_resume_only():
    """Score resume based on provided data"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided',
                'message': 'Please provide resume text to score'
            }), 400
        
        text = data['text']
        language = data.get('language', 'en')
        skills = data.get('skills', [])
        experience = data.get('experience', [])
        education = data.get('education', [])
        
        scores = scorer.calculate_scores(
            text,
            skills,
            experience,
            education,
            language
        )
        
        return jsonify({
            'success': True,
            'scores': scores
        })
        
    except Exception as e:
        app.logger.error(f'Error scoring resume: {str(e)}')
        return jsonify({
            'error': 'Scoring failed',
            'message': str(e)
        }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    """Rate limit exceeded handler"""
    return jsonify({
        'error': 'Rate limit exceeded',
        'message': 'Too many requests. Please try again later.'
    }), 429

@app.errorhandler(404)
def not_found_handler(e):
    """Not found handler"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error_handler(e):
    """Internal error handler"""
    app.logger.error(f'Internal server error: {str(e)}')
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=app.debug)
