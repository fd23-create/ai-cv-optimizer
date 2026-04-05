import os
import magic
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ResumeValidator:
    """Validator for resume files and content"""
    
    def __init__(self):
        self.max_file_size = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
        self.supported_formats = {
            'application/pdf': ['.pdf'],
            'application/msword': ['.doc'],
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
        }
        self.min_text_length = 100
        self.max_text_length = 50000
    
    def validate_file(self, file) -> Dict[str, Any]:
        """
        Validate uploaded file
        
        Args:
            file: File object from Flask request
            
        Returns:
            Dictionary with validation result
        """
        try:
            # Check if file exists
            if not file or not file.filename:
                return {
                    'valid': False,
                    'message': 'No file provided',
                    'error_code': 'NO_FILE'
                }
            
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > self.max_file_size:
                return {
                    'valid': False,
                    'message': f'File too large. Maximum size is {self.max_file_size / (1024*1024):.1f}MB',
                    'error_code': 'FILE_TOO_LARGE',
                    'file_size': file_size
                }
            
            if file_size < 1024:  # At least 1KB
                return {
                    'valid': False,
                    'message': 'File too small. Minimum size is 1KB',
                    'error_code': 'FILE_TOO_SMALL',
                    'file_size': file_size
                }
            
            # Check file extension
            file_extension = self._get_file_extension(file.filename)
            if not self._is_supported_extension(file_extension):
                return {
                    'valid': False,
                    'message': f'Unsupported file format: {file_extension}. Supported formats: PDF, DOC, DOCX',
                    'error_code': 'UNSUPPORTED_FORMAT',
                    'file_extension': file_extension
                }
            
            # Check MIME type
            mime_type = self._get_mime_type(file)
            if not self._is_supported_mime_type(mime_type):
                return {
                    'valid': False,
                    'message': f'Unsupported file type: {mime_type}',
                    'error_code': 'UNSUPPORTED_MIME_TYPE',
                    'mime_type': mime_type
                }
            
            return {
                'valid': True,
                'message': 'File validation passed',
                'file_size': file_size,
                'file_extension': file_extension,
                'mime_type': mime_type
            }
            
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}")
            return {
                'valid': False,
                'message': 'File validation failed',
                'error_code': 'VALIDATION_ERROR',
                'error': str(e)
            }
    
    def validate_text_content(self, text: str) -> Dict[str, Any]:
        """
        Validate extracted text content
        
        Args:
            text: Extracted text content
            
        Returns:
            Dictionary with validation result
        """
        try:
            if not text:
                return {
                    'valid': False,
                    'message': 'No text content found',
                    'error_code': 'NO_TEXT'
                }
            
            text_length = len(text.strip())
            
            # Check minimum length
            if text_length < self.min_text_length:
                return {
                    'valid': False,
                    'message': f'Text too short. Minimum length is {self.min_text_length} characters',
                    'error_code': 'TEXT_TOO_SHORT',
                    'text_length': text_length
                }
            
            # Check maximum length
            if text_length > self.max_text_length:
                return {
                    'valid': False,
                    'message': f'Text too long. Maximum length is {self.max_text_length} characters',
                    'error_code': 'TEXT_TOO_LONG',
                    'text_length': text_length
                }
            
            # Check for meaningful content
            if not self._has_meaningful_content(text):
                return {
                    'valid': False,
                    'message': 'Text appears to contain only special characters or formatting',
                    'error_code': 'INVALID_CONTENT'
                }
            
            return {
                'valid': True,
                'message': 'Text validation passed',
                'text_length': text_length,
                'word_count': len(text.split()),
                'has_meaningful_content': True
            }
            
        except Exception as e:
            logger.error(f"Error validating text content: {str(e)}")
            return {
                'valid': False,
                'message': 'Text validation failed',
                'error_code': 'VALIDATION_ERROR',
                'error': str(e)
            }
    
    def validate_resume_structure(self, text: str) -> Dict[str, Any]:
        """
        Validate resume structure and sections
        
        Args:
            text: Resume text content
            
        Returns:
            Dictionary with structure validation result
        """
        try:
            if not text:
                return {
                    'valid': False,
                    'message': 'No text to validate',
                    'sections': [],
                    'issues': ['No text provided']
                }
            
            text_lower = text.lower()
            
            # Define expected sections
            expected_sections = {
                'experience': ['experience', 'work experience', 'professional experience', 'employment', 
                              'expériences', 'expérience professionnelle', 'emploi'],
                'education': ['education', 'academic', 'training', 'formation', 'éducation', 'académique'],
                'skills': ['skills', 'competencies', 'abilities', 'compétences', 'aptitudes'],
                'summary': ['summary', 'profile', 'objective', 'about', 'résumé', 'profil', 'objectif'],
                'contact': ['contact', 'email', 'phone', 'téléphone', 'email', 'courriel']
            }
            
            found_sections = []
            missing_sections = []
            
            for section, keywords in expected_sections.items():
                found = any(keyword in text_lower for keyword in keywords)
                if found:
                    found_sections.append(section)
                else:
                    missing_sections.append(section)
            
            # Check for contact information
            has_email = '@' in text_lower and '.' in text_lower
            has_phone = any(char.isdigit() for char in text) and len(text) > 100
            
            contact_issues = []
            if not has_email:
                contact_issues.append('No email address detected')
            if not has_phone:
                contact_issues.append('No phone number detected')
            
            # Check for dates (indicating experience/education timeline)
            import re
            date_pattern = r'\b(19|20)\d{2}\b'
            dates = re.findall(date_pattern, text)
            
            if len(dates) < 2:
                missing_sections.append('timeline')
            
            # Calculate structure score
            total_expected = len(expected_sections)
            found_count = len(found_sections)
            structure_score = (found_count / total_expected) * 100
            
            # Determine validity
            issues = []
            if len(found_sections) < 2:
                issues.append('Too few resume sections detected')
            
            if len(contact_issues) > 0:
                issues.extend(contact_issues)
            
            if len(dates) < 2:
                issues.append('Few or no dates found in resume')
            
            is_valid = len(issues) == 0 and structure_score >= 40
            
            return {
                'valid': is_valid,
                'structure_score': structure_score,
                'found_sections': found_sections,
                'missing_sections': missing_sections,
                'issues': issues,
                'has_contact_info': has_email or has_phone,
                'date_count': len(dates),
                'word_count': len(text.split())
            }
            
        except Exception as e:
            logger.error(f"Error validating resume structure: {str(e)}")
            return {
                'valid': False,
                'message': 'Structure validation failed',
                'sections': [],
                'issues': [str(e)]
            }
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        return filename.lower().split('.')[-1] if '.' in filename else ''
    
    def _is_supported_extension(self, extension: str) -> bool:
        """Check if file extension is supported"""
        supported_extensions = []
        for extensions in self.supported_formats.values():
            supported_extensions.extend(extensions)
        
        return extension in supported_extensions
    
    def _get_mime_type(self, file) -> Optional[str]:
        """Get MIME type of file"""
        try:
            # Read first few bytes to detect MIME type
            file.seek(0)
            header = file.read(1024)
            file.seek(0)
            
            # Use python-magic if available
            try:
                mime = magic.Magic(mime=True)
                return mime.from_buffer(header)
            except ImportError:
                # Fallback to basic MIME type detection
                return self._basic_mime_detection(header, file.filename)
                
        except Exception as e:
            logger.error(f"Error detecting MIME type: {str(e)}")
            return None
    
    def _basic_mime_detection(self, header: bytes, filename: str) -> Optional[str]:
        """Basic MIME type detection fallback"""
        extension = self._get_file_extension(filename)
        
        if extension == 'pdf':
            return 'application/pdf'
        elif extension in ['doc', 'docx']:
            return 'application/msword' if extension == 'doc' else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        
        return None
    
    def _is_supported_mime_type(self, mime_type: Optional[str]) -> bool:
        """Check if MIME type is supported"""
        return mime_type in self.supported_formats.keys()
    
    def _has_meaningful_content(self, text: str) -> bool:
        """Check if text contains meaningful content"""
        if not text:
            return False
        
        # Remove whitespace and special characters
        clean_text = ''.join(char for char in text if char.isalnum() or char.isspace())
        
        # Check if we have enough alphanumeric characters
        if len(clean_text) < 50:
            return False
        
        # Check for common words (basic content validation)
        common_words = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        text_lower = clean_text.lower()
        
        found_common = sum(1 for word in common_words if word in text_lower)
        
        # Should have at least some common words
        return found_common >= 2
    
    def get_validation_summary(self, file_result: Dict[str, Any], 
                             text_result: Dict[str, Any], 
                             structure_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get comprehensive validation summary
        
        Args:
            file_result: File validation result
            text_result: Text validation result
            structure_result: Structure validation result
            
        Returns:
            Summary validation result
        """
        try:
            all_valid = all([
                file_result.get('valid', False),
                text_result.get('valid', False),
                structure_result.get('valid', False)
            ])
            
            all_issues = []
            all_issues.extend(file_result.get('issues', []))
            all_issues.extend(text_result.get('issues', []))
            all_issues.extend(structure_result.get('issues', []))
            
            # Add error messages if present
            if file_result.get('message') and not file_result.get('valid'):
                all_issues.append(file_result['message'])
            if text_result.get('message') and not text_result.get('valid'):
                all_issues.append(text_result['message'])
            if structure_result.get('message') and not structure_result.get('valid'):
                all_issues.append(structure_result['message'])
            
            return {
                'valid': all_valid,
                'overall_score': structure_result.get('structure_score', 0),
                'issues': all_issues,
                'file_info': {
                    'size': file_result.get('file_size'),
                    'extension': file_result.get('file_extension'),
                    'mime_type': file_result.get('mime_type')
                },
                'text_info': {
                    'length': text_result.get('text_length'),
                    'word_count': text_result.get('word_count')
                },
                'structure_info': {
                    'sections': structure_result.get('found_sections', []),
                    'missing_sections': structure_result.get('missing_sections', []),
                    'has_contact_info': structure_result.get('has_contact_info', False)
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating validation summary: {str(e)}")
            return {
                'valid': False,
                'issues': ['Validation summary failed'],
                'error': str(e)
            }
