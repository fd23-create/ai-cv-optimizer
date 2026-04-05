import re
import string
import logging
from typing import List, Dict, Optional
from langdetect import detect
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

logger = logging.getLogger(__name__)

class TextCleaner:
    """Text cleaning and preprocessing utilities"""
    
    def __init__(self):
        self.stop_words = {}
        self._load_stop_words()
    
    def _load_stop_words(self):
        """Load stop words for different languages"""
        try:
            # Download NLTK data if not available
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            # Load stop words for supported languages
            languages = ['english', 'french', 'spanish', 'german', 'italian', 'portuguese']
            for lang in languages:
                try:
                    self.stop_words[lang[:2]] = set(stopwords.words(lang))
                except OSError:
                    logger.warning(f"Stop words for {lang} not available")
                    self.stop_words[lang[:2]] = set()
                    
        except Exception as e:
            logger.error(f"Error loading stop words: {str(e)}")
            self.stop_words = {'en': set(), 'fr': set(), 'es': set(), 'de': set(), 'it': set(), 'pt': set()}
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\{\}\"\'\/\%\&\@\#\$\*\+\=]', ' ', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])\s+', r'\1 ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Strip and return
        return text.strip()
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code (en, fr, es, de, it, pt)
        """
        if not text or len(text.strip()) < 50:
            return 'en'  # Default to English
        
        try:
            # Use langdetect for primary detection
            detected = detect(text)
            
            # Map to supported languages
            lang_mapping = {
                'en': 'en', 'fr': 'fr', 'es': 'es', 
                'de': 'de', 'it': 'it', 'pt': 'pt'
            }
            
            return lang_mapping.get(detected, 'en')
            
        except Exception as e:
            logger.warning(f"Language detection failed: {str(e)}")
            return 'en'
    
    def remove_stop_words(self, text: str, language: str = 'en') -> str:
        """
        Remove stop words from text
        
        Args:
            text: Text to process
            language: Language code
            
        Returns:
            Text without stop words
        """
        if not text:
            return ""
        
        try:
            words = word_tokenize(text.lower())
            stop_words = self.stop_words.get(language, set())
            
            filtered_words = [word for word in words if word not in stop_words]
            
            return ' '.join(filtered_words)
            
        except Exception as e:
            logger.error(f"Error removing stop words: {str(e)}")
            return text
    
    def tokenize_text(self, text: str, language: str = 'en') -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            language: Language code
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        try:
            tokens = word_tokenize(text.lower())
            
            # Remove punctuation and short tokens
            tokens = [
                token for token in tokens 
                if token not in string.punctuation and len(token) > 1
            ]
            
            return tokens
            
        except Exception as e:
            logger.error(f"Error tokenizing text: {str(e)}")
            return text.lower().split()
    
    def extract_sentences(self, text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Text to process
            
        Returns:
            List of sentences
        """
        if not text:
            return []
        
        try:
            sentences = sent_tokenize(text)
            return [sent.strip() for sent in sentences if sent.strip()]
            
        except Exception as e:
            logger.error(f"Error extracting sentences: {str(e)}")
            # Fallback to simple split
            return [sent.strip() for sent in text.split('.') if sent.strip()]
    
    def normalize_text(self, text: str, language: str = 'en') -> str:
        """
        Normalize text (lowercase, remove accents, etc.)
        
        Args:
            text: Text to normalize
            language: Language code
            
        Returns:
            Normalized text
        """
        if not text:
            return ""
        
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove accents for better matching
            if language in ['fr', 'es', 'de', 'it', 'pt']:
                import unicodedata
                text = unicodedata.normalize('NFD', text)
                text = unicodedata.normalize('NFC', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error normalizing text: {str(e)}")
            return text.lower()
    
    def extract_keywords(self, text: str, language: str = 'en', max_keywords: int = 20) -> List[str]:
        """
        Extract keywords from text using TextBlob
        
        Args:
            text: Text to analyze
            language: Language code
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of keywords
        """
        if not text:
            return []
        
        try:
            # Clean and normalize text
            clean_text = self.clean_text(text)
            normalized_text = self.normalize_text(clean_text, language)
            
            # Use TextBlob for noun phrase extraction
            blob = TextBlob(normalized_text)
            
            # Extract noun phrases as keywords
            noun_phrases = blob.noun_phrases
            
            # Remove stop words and short phrases
            stop_words = self.stop_words.get(language, set())
            keywords = []
            
            for phrase in noun_phrases:
                words = phrase.split()
                if len(words) <= 3 and len(phrase) > 2:  # Max 3 words, min 2 chars
                    if not any(word in stop_words for word in words):
                        keywords.append(phrase)
            
            # Remove duplicates and limit
            unique_keywords = list(dict.fromkeys(keywords))
            return unique_keywords[:max_keywords]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    def calculate_readability_score(self, text: str, language: str = 'en') -> Dict[str, float]:
        """
        Calculate readability scores
        
        Args:
            text: Text to analyze
            language: Language code
            
        Returns:
            Dictionary with readability metrics
        """
        if not text:
            return {'score': 0.0, 'avg_sentence_length': 0.0, 'avg_word_length': 0.0}
        
        try:
            sentences = self.extract_sentences(text)
            words = self.tokenize_text(text, language)
            
            if not sentences or not words:
                return {'score': 0.0, 'avg_sentence_length': 0.0, 'avg_word_length': 0.0}
            
            # Calculate metrics
            avg_sentence_length = len(words) / len(sentences)
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Simple readability score (based on sentence and word length)
            # Higher score = more readable
            sentence_score = min(1.0, 20.0 / avg_sentence_length)  # Ideal: ~20 words per sentence
            word_score = min(1.0, 5.0 / avg_word_length)  # Ideal: ~5 characters per word
            
            overall_score = (sentence_score + word_score) / 2
            
            return {
                'score': overall_score,
                'avg_sentence_length': avg_sentence_length,
                'avg_word_length': avg_word_length,
                'sentence_count': len(sentences),
                'word_count': len(words)
            }
            
        except Exception as e:
            logger.error(f"Error calculating readability: {str(e)}")
            return {'score': 0.0, 'avg_sentence_length': 0.0, 'avg_word_length': 0.0}
    
    def extract_contact_info(self, text: str) -> Dict[str, List[str]]:
        """
        Extract contact information from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with extracted contact info
        """
        contact_info = {
            'emails': [],
            'phones': [],
            'websites': [],
            'linkedin': []
        }
        
        if not text:
            return contact_info
        
        try:
            # Email patterns
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text, re.IGNORECASE)
            contact_info['emails'] = list(set(emails))
            
            # Phone patterns (various formats)
            phone_patterns = [
                r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US format
                r'\b\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',  # International
                r'\b\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}\b'  # US with parentheses
            ]
            
            phones = []
            for pattern in phone_patterns:
                phones.extend(re.findall(pattern, text))
            contact_info['phones'] = list(set(phones))
            
            # Website patterns
            website_pattern = r'\b(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            websites = re.findall(website_pattern, text, re.IGNORECASE)
            contact_info['websites'] = list(set(websites))
            
            # LinkedIn specific pattern
            linkedin_pattern = r'\b(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9-]+\b'
            linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
            contact_info['linkedin'] = list(set(linkedin))
            
        except Exception as e:
            logger.error(f"Error extracting contact info: {str(e)}")
        
        return contact_info
    
    def clean_resume_section(self, text: str, section_type: str) -> str:
        """
        Clean specific resume sections
        
        Args:
            text: Section text
            section_type: Type of section (experience, education, skills, etc.)
            
        Returns:
            Cleaned section text
        """
        if not text:
            return ""
        
        try:
            # Remove common section headers
            header_patterns = [
                r'^(experience|expériences|education|formation|skills|compétences|summary|résumé)',
                r'^(profile|profil|objective|objectif|about|à propos)',
                r'^(work experience|expérience professionnelle|employment|emploi)',
                r'^(academic|académique|training|formation professionnelle)'
            ]
            
            for pattern in header_patterns:
                text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            
            # Section-specific cleaning
            if section_type == 'experience':
                # Remove bullet points and normalize dates
                text = re.sub(r'^[•\-\*]\s*', '', text, flags=re.MULTILINE)
                text = re.sub(r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2,4})', r'\1/\2/\3', text)
                
            elif section_type == 'education':
                # Normalize degree names and institutions
                text = re.sub(r'\b(bachelor|master|phd|doctorate|licence|master|doctorat)\b', 
                             lambda m: m.group(0).title(), text, flags=re.IGNORECASE)
                
            elif section_type == 'skills':
                # Split skills into consistent format
                text = re.sub(r'[,;]\s*', ', ', text)
                text = re.sub(r'\s+', ' ', text)
            
            return self.clean_text(text)
            
        except Exception as e:
            logger.error(f"Error cleaning resume section: {str(e)}")
            return self.clean_text(text)
