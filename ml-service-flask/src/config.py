import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for ML Service"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Redis Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Model Configuration
    MODEL_PATH = os.getenv('MODEL_PATH', './models')
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')
    SENTENCE_TRANSFORMER_MODEL = os.getenv('SENTENCE_TRANSFORMER_MODEL', 'all-MiniLM-L6-v2')
    
    # Analysis Configuration
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'en,fr,es,de,it,pt').split(',')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/ml_service.log')
    
    # Rate Limiting
    RATE_LIMIT = os.getenv('RATE_LIMIT', '100/hour')
    
    # Cache Configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 3600))
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    # Processing Configuration
    MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', 50000))  # Max characters to process
    MIN_EXPERIENCE_YEARS = int(os.getenv('MIN_EXPERIENCE_YEARS', 0))
    MAX_EXPERIENCE_YEARS = int(os.getenv('MAX_EXPERIENCE_YEARS', 50))
    
    # Scoring Configuration
    SKILLS_WEIGHT = float(os.getenv('SKILLS_WEIGHT', 0.3))
    EXPERIENCE_WEIGHT = float(os.getenv('EXPERIENCE_WEIGHT', 0.3))
    EDUCATION_WEIGHT = float(os.getenv('EDUCATION_WEIGHT', 0.2))
    FORMAT_WEIGHT = float(os.getenv('FORMAT_WEIGHT', 0.2))
    
    # AI Generation Configuration
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 1000))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration values"""
        required_vars = ['OPENAI_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Validate weights sum to 1.0
        total_weight = cls.SKILLS_WEIGHT + cls.EXPERIENCE_WEIGHT + cls.EDUCATION_WEIGHT + cls.FORMAT_WEIGHT
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Scoring weights must sum to 1.0, got {total_weight}")
        
        return True
    
    @classmethod
    def get_language_config(cls, language):
        """Get language-specific configuration"""
        configs = {
            'en': {
                'spacy_model': 'en_core_web_sm',
                'stop_words_file': 'stopwords_en.txt',
                'skills_keywords': 'skills_en.json'
            },
            'fr': {
                'spacy_model': 'fr_core_news_sm',
                'stop_words_file': 'stopwords_fr.txt',
                'skills_keywords': 'skills_fr.json'
            },
            'es': {
                'spacy_model': 'es_core_news_sm',
                'stop_words_file': 'stopwords_es.txt',
                'skills_keywords': 'skills_es.json'
            },
            'de': {
                'spacy_model': 'de_core_news_sm',
                'stop_words_file': 'stopwords_de.txt',
                'skills_keywords': 'skills_de.json'
            },
            'it': {
                'spacy_model': 'it_core_news_sm',
                'stop_words_file': 'stopwords_it.txt',
                'skills_keywords': 'skills_it.json'
            },
            'pt': {
                'spacy_model': 'pt_core_news_sm',
                'stop_words_file': 'stopwords_pt.txt',
                'skills_keywords': 'skills_pt.json'
            }
        }
        
        return configs.get(language, configs['en'])
