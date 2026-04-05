import re
import logging
from typing import Dict, List, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

class ResumeScorer:
    """Resume scoring and evaluation system"""
    
    def __init__(self):
        self.weights = {
            'skills': 0.30,
            'experience': 0.30,
            'education': 0.20,
            'format': 0.20
        }
        
        # Industry-specific keywords (simplified)
        self.industry_keywords = {
            'technology': ['software', 'programming', 'development', 'coding', 'api', 'database', 'cloud', 'devops'],
            'healthcare': ['medical', 'healthcare', 'patient', 'clinical', 'hospital', 'nursing', 'pharmacy'],
            'finance': ['financial', 'banking', 'investment', 'accounting', 'finance', 'trading', 'risk'],
            'marketing': ['marketing', 'advertising', 'brand', 'campaign', 'social media', 'content', 'seo'],
            'education': ['teaching', 'education', 'learning', 'curriculum', 'students', 'academic', 'training']
        }
        
        # Common action verbs for resumes
        self.action_verbs = [
            'managed', 'led', 'developed', 'implemented', 'created', 'designed', 'analyzed',
            'optimized', 'improved', 'increased', 'reduced', 'achieved', 'coordinated', 'trained',
            'mentored', 'collaborated', 'negotiated', 'presented', 'researched', 'evaluated'
        ]
    
    def calculate_scores(self, text: str, skills: List[Dict], experience: List[Dict], 
                        education: List[Dict], language: str = 'en') -> Dict[str, Any]:
        """
        Calculate comprehensive resume scores
        
        Args:
            text: Full resume text
            skills: Extracted skills
            experience: Extracted experience
            education: Extracted education
            language: Language code
            
        Returns:
            Dictionary with all scores
        """
        try:
            # Calculate individual component scores
            skills_score = self._calculate_skills_score(text, skills, language)
            experience_score = self._calculate_experience_score(text, experience, language)
            education_score = self._calculate_education_score(text, education, language)
            format_score = self._calculate_format_score(text, language)
            
            # Calculate weighted overall score
            overall_score = (
                skills_score * self.weights['skills'] +
                experience_score * self.weights['experience'] +
                education_score * self.weights['education'] +
                format_score * self.weights['format']
            )
            
            # Determine industry relevance
            industry_match = self._calculate_industry_relevance(text)
            
            # Calculate action verb usage
            action_verb_score = self._calculate_action_verb_score(text)
            
            # Calculate keyword density
            keyword_density = self._calculate_keyword_density(text)
            
            return {
                'overall': round(overall_score, 1),
                'skills': round(skills_score, 1),
                'experience': round(experience_score, 1),
                'education': round(education_score, 1),
                'format': round(format_score, 1),
                'industry_match': industry_match,
                'action_verb_score': round(action_verb_score, 1),
                'keyword_density': round(keyword_density, 1),
                'breakdown': {
                    'skills': {
                        'score': round(skills_score, 1),
                        'weight': self.weights['skills'],
                        'contribution': round(skills_score * self.weights['skills'], 1)
                    },
                    'experience': {
                        'score': round(experience_score, 1),
                        'weight': self.weights['experience'],
                        'contribution': round(experience_score * self.weights['experience'], 1)
                    },
                    'education': {
                        'score': round(education_score, 1),
                        'weight': self.weights['education'],
                        'contribution': round(education_score * self.weights['education'], 1)
                    },
                    'format': {
                        'score': round(format_score, 1),
                        'weight': self.weights['format'],
                        'contribution': round(format_score * self.weights['format'], 1)
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating scores: {str(e)}")
            return {
                'overall': 0.0,
                'skills': 0.0,
                'experience': 0.0,
                'education': 0.0,
                'format': 0.0,
                'error': str(e)
            }
    
    def _calculate_skills_score(self, text: str, skills: List[Dict], language: str) -> float:
        """Calculate skills-related score"""
        try:
            if not skills:
                return 20.0  # Minimum score if no skills found
            
            # Base score from number of skills
            skill_count_score = min(len(skills) * 5, 40)  # Max 40 points for quantity
            
            # Score from skill variety (different categories)
            skill_categories = set(skill.get('category', 'unknown') for skill in skills)
            variety_score = min(len(skill_categories) * 10, 30)  # Max 30 points for variety
            
            # Score from skill levels
            skill_levels = [skill.get('level', 0) for skill in skills if skill.get('level')]
            if skill_levels:
                avg_level = sum(skill_levels) / len(skill_levels)
                level_score = avg_level * 3  # Max 30 points for skill levels
            else:
                level_score = 15.0  # Average score if no levels specified
            
            # Total skills score (max 100)
            total_score = skill_count_score + variety_score + level_score
            
            return min(total_score, 100.0)
            
        except Exception as e:
            logger.error(f"Error calculating skills score: {str(e)}")
            return 20.0
    
    def _calculate_experience_score(self, text: str, experience: List[Dict], language: str) -> float:
        """Calculate experience-related score"""
        try:
            if not experience:
                return 20.0  # Minimum score if no experience found
            
            # Score from number of positions
            position_count_score = min(len(experience) * 15, 30)  # Max 30 points
            
            # Score from total experience duration
            total_years = 0
            for exp in experience:
                duration = exp.get('duration_years', 0)
                total_years += duration
            
            duration_score = min(total_years * 5, 40)  # Max 40 points for experience
            
            # Score from experience quality (descriptions, achievements)
            quality_score = 0
            for exp in experience:
                description = exp.get('description', '')
                if description:
                    # Check for quantifiable achievements
                    if re.search(r'\d+%|\$\d+|\d+\s*(years?|months?)', description, re.IGNORECASE):
                        quality_score += 10
                    # Check for action verbs
                    action_count = sum(1 for verb in self.action_verbs if verb.lower() in description.lower())
                    quality_score += min(action_count * 2, 10)
            
            quality_score = min(quality_score, 30)  # Max 30 points for quality
            
            # Total experience score (max 100)
            total_score = position_count_score + duration_score + quality_score
            
            return min(total_score, 100.0)
            
        except Exception as e:
            logger.error(f"Error calculating experience score: {str(e)}")
            return 20.0
    
    def _calculate_education_score(self, text: str, education: List[Dict], language: str) -> float:
        """Calculate education-related score"""
        try:
            if not education:
                return 20.0  # Minimum score if no education found
            
            # Score from education level
            level_scores = {
                'high_school': 20,
                'associate': 40,
                'bachelor': 70,
                'master': 85,
                'phd': 95,
                'doctorate': 95
            }
            
            max_level_score = 0
            for edu in education:
                level = edu.get('level', '').lower()
                for key, score in level_scores.items():
                    if key in level:
                        max_level_score = max(max_level_score, score)
                        break
            
            # Score from number of degrees
            degree_count_score = min(len(education) * 10, 20)  # Max 20 points
            
            # Score from relevance (if field is specified)
            relevance_score = 0
            for edu in education:
                field = edu.get('field', '').lower()
                if any(keyword in field for keyword in ['computer', 'business', 'engineering', 'science']):
                    relevance_score += 10
            
            relevance_score = min(relevance_score, 10)  # Max 10 points for relevance
            
            # Total education score (max 100)
            total_score = max_level_score + degree_count_score + relevance_score
            
            return min(total_score, 100.0)
            
        except Exception as e:
            logger.error(f"Error calculating education score: {str(e)}")
            return 20.0
    
    def _calculate_format_score(self, text: str, language: str) -> float:
        """Calculate format and structure score"""
        try:
            score = 0
            
            # Check for proper structure (20 points)
            sections = ['experience', 'education', 'skills']
            found_sections = sum(1 for section in sections if section.lower() in text.lower())
            score += min(found_sections * 7, 20)
            
            # Check for contact information (15 points)
            has_email = '@' in text and '.' in text
            has_phone = bool(re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', text))
            
            if has_email:
                score += 8
            if has_phone:
                score += 7
            
            # Check for proper length (15 points)
            word_count = len(text.split())
            if 200 <= word_count <= 800:
                score += 15
            elif 100 <= word_count < 200 or 800 < word_count <= 1200:
                score += 10
            elif word_count >= 1200:
                score += 5
            
            # Check for bullet points and formatting (20 points)
            bullet_patterns = [r'•', r'\*', r'-', r'\d+\.', r'\([a-z]\)']
            bullet_count = sum(len(re.findall(pattern, text)) for pattern in bullet_patterns)
            score += min(bullet_count * 2, 20)
            
            # Check for action verbs (15 points)
            action_verb_count = sum(1 for verb in self.action_verbs if verb.lower() in text.lower())
            score += min(action_verb_count, 15)
            
            # Check for quantifiable achievements (15 points)
            quantifiable_patterns = [
                r'\d+%', r'\$\d+', r'\d+\s*(years?|months?)', r'\d+\s*(people|employees|clients)'
            ]
            quantifiable_count = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in quantifiable_patterns)
            score += min(quantifiable_count * 3, 15)
            
            return min(score, 100.0)
            
        except Exception as e:
            logger.error(f"Error calculating format score: {str(e)}")
            return 20.0
    
    def _calculate_industry_relevance(self, text: str) -> Dict[str, Any]:
        """Calculate industry relevance score"""
        try:
            text_lower = text.lower()
            relevance_scores = {}
            
            for industry, keywords in self.industry_keywords.items():
                keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
                relevance_scores[industry] = keyword_count
            
            # Find best matching industry
            if relevance_scores:
                best_industry = max(relevance_scores, key=relevance_scores.get)
                best_score = relevance_scores[best_industry]
            else:
                best_industry = 'general'
                best_score = 0
            
            return {
                'best_industry': best_industry,
                'score': best_score,
                'all_scores': relevance_scores
            }
            
        except Exception as e:
            logger.error(f"Error calculating industry relevance: {str(e)}")
            return {'best_industry': 'general', 'score': 0, 'all_scores': {}}
    
    def _calculate_action_verb_score(self, text: str) -> float:
        """Calculate action verb usage score"""
        try:
            text_lower = text.lower()
            action_verb_count = sum(1 for verb in self.action_verbs if verb in text_lower)
            
            # Normalize by text length (approximately)
            word_count = len(text.split())
            if word_count == 0:
                return 0.0
            
            # Calculate action verb density
            verb_density = (action_verb_count / word_count) * 100
            
            # Score based on density (optimal range: 5-15%)
            if 5 <= verb_density <= 15:
                return 100.0
            elif verb_density < 5:
                return (verb_density / 5) * 100
            else:
                return max(50, 100 - (verb_density - 15) * 5)
            
        except Exception as e:
            logger.error(f"Error calculating action verb score: {str(e)}")
            return 0.0
    
    def _calculate_keyword_density(self, text: str) -> float:
        """Calculate keyword density score"""
        try:
            # Extract keywords using TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            try:
                tfidf_matrix = vectorizer.fit_transform([text])
                feature_names = vectorizer.get_feature_names_out()
                tfidf_scores = tfidf_matrix.toarray()[0]
                
                # Calculate average TF-IDF score
                if len(tfidf_scores) > 0:
                    avg_score = np.mean(tfidf_scores)
                    # Normalize to 0-100 scale
                    normalized_score = min(avg_score * 1000, 100)  # Scaling factor
                    return round(normalized_score, 1)
                else:
                    return 0.0
                    
            except Exception:
                # Fallback to simple keyword counting
                words = text.lower().split()
                word_freq = {}
                for word in words:
                    if len(word) > 3:  # Ignore very short words
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                if word_freq:
                    # Calculate average frequency
                    avg_freq = sum(word_freq.values()) / len(word_freq)
                    return min(avg_freq * 10, 100)  # Simple scaling
                else:
                    return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating keyword density: {str(e)}")
            return 0.0
    
    def get_score_interpretation(self, score: float) -> Dict[str, Any]:
        """
        Get interpretation of score
        
        Args:
            score: Score value (0-100)
            
        Returns:
            Dictionary with score interpretation
        """
        try:
            if score >= 90:
                level = 'Excellent'
                description = 'Outstanding resume that meets all professional standards'
                recommendations = ['Maintain current quality', 'Consider customizing for specific roles']
            elif score >= 80:
                level = 'Very Good'
                description = 'Strong resume with minor areas for improvement'
                recommendations = ['Add more quantifiable achievements', 'Enhance skill descriptions']
            elif score >= 70:
                level = 'Good'
                description = 'Solid resume that could benefit from some enhancements'
                recommendations = ['Improve structure and formatting', 'Add more specific examples']
            elif score >= 60:
                level = 'Average'
                description = 'Acceptable resume that needs significant improvements'
                recommendations = ['Revise content and structure', 'Add missing sections']
            elif score >= 50:
                level = 'Below Average'
                description = 'Resume requires major improvements'
                recommendations = ['Complete rewrite recommended', 'Seek professional help']
            else:
                level = 'Poor'
                description = 'Resume needs fundamental changes'
                recommendations = ['Complete reconstruction required', 'Consider professional resume service']
            
            return {
                'level': level,
                'score': score,
                'description': description,
                'recommendations': recommendations,
                'color': self._get_score_color(score)
            }
            
        except Exception as e:
            logger.error(f"Error interpreting score: {str(e)}")
            return {
                'level': 'Unknown',
                'score': score,
                'description': 'Unable to interpret score',
                'recommendations': [],
                'color': '#666666'
            }
    
    def _get_score_color(self, score: float) -> str:
        """Get color code for score"""
        if score >= 80:
            return '#10b981'  # Green
        elif score >= 60:
            return '#3b82f6'  # Blue
        elif score >= 40:
            return '#f59e0b'  # Yellow
        else:
            return '#ef4444'  # Red
