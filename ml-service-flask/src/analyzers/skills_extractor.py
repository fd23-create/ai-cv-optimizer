import re
import json
import logging
from typing import Dict, List, Any, Optional
from collections import Counter
import yake
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

logger = logging.getLogger(__name__)

class SkillsExtractor:
    """Advanced skills extraction system"""
    
    def __init__(self):
        # Load spaCy model (will be loaded lazily)
        self.nlp = None
        self.spacy_model = 'en_core_web_sm'
        
        # Skill categories and keywords
        self.skill_categories = {
            'technical': {
                'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust'],
                'web_development': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring'],
                'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle'],
                'cloud': ['aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
                'data_science': ['machine learning', 'data analysis', 'statistics', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
                'mobile': ['ios', 'android', 'react native', 'flutter', 'swift', 'kotlin', 'xamarin', 'cordova']
            },
            'business': {
                'management': ['project management', 'team leadership', 'strategic planning', 'resource management', 'agile', 'scrum'],
                'marketing': ['digital marketing', 'seo', 'sem', 'content marketing', 'social media', 'email marketing', 'analytics'],
                'sales': ['business development', 'account management', 'negotiation', 'client relations', 'sales strategy'],
                'finance': ['financial analysis', 'budgeting', 'accounting', 'risk management', 'investment', 'forecasting'],
                'operations': ['supply chain', 'logistics', 'quality control', 'process improvement', 'lean manufacturing']
            },
            'soft_skills': {
                'communication': ['public speaking', 'presentation', 'writing', 'interpersonal communication', 'negotiation'],
                'leadership': ['team building', 'mentoring', 'delegation', 'decision making', 'conflict resolution'],
                'problem_solving': ['critical thinking', 'analytical skills', 'creativity', 'innovation', 'troubleshooting'],
                'collaboration': ['teamwork', 'cross-functional', 'partnership', 'stakeholder management', 'collaboration'],
                'adaptability': ['flexibility', 'change management', 'learning agility', 'resilience', 'versatility']
            },
            'tools': {
                'office': ['microsoft office', 'excel', 'powerpoint', 'word', 'outlook', 'google workspace', 'slack'],
                'design': ['photoshop', 'illustrator', 'figma', 'sketch', 'adobe creative suite', 'ui/ux design'],
                'development_tools': ['git', 'github', 'gitlab', 'jira', 'confluence', 'vs code', 'intellij'],
                'analytics': ['google analytics', 'tableau', 'power bi', 'excel advanced', 'sql analytics']
            }
        }
        
        # Create flattened skill list for easy matching
        self.all_skills = []
        for category, subcategories in self.skill_categories.items():
            for subcategory, skills in subcategories.items():
                for skill in skills:
                    self.all_skills.append({
                        'skill': skill,
                        'category': category,
                        'subcategory': subcategory
                    })
    
    def _load_spacy_model(self):
        """Load spaCy model lazily"""
        if self.nlp is None:
            try:
                import spacy
                self.nlp = spacy.load(self.spacy_model)
                logger.info(f"Loaded spaCy model: {self.spacy_model}")
            except OSError:
                logger.warning(f"spaCy model {self.spacy_model} not found, using basic extraction")
                self.nlp = None
    
    def extract_skills(self, text: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Extract skills from resume text
        
        Args:
            text: Resume text
            language: Language code
            
        Returns:
            List of extracted skills with metadata
        """
        try:
            # Clean and normalize text
            clean_text = self._clean_text(text)
            
            # Extract skills using multiple methods
            keyword_skills = self._extract_keyword_skills(clean_text)
            pattern_skills = self._extract_pattern_skills(clean_text)
            entity_skills = self._extract_entity_skills(clean_text)
            yake_skills = self._extract_yake_skills(clean_text)
            
            # Combine and deduplicate skills
            all_extracted = keyword_skills + pattern_skills + entity_skills + yake_skills
            
            # Deduplicate and rank skills
            unique_skills = self._deduplicate_skills(all_extracted)
            ranked_skills = self._rank_skills(unique_skills, clean_text)
            
            return ranked_skills[:50]  # Return top 50 skills
            
        except Exception as e:
            logger.error(f"Error extracting skills: {str(e)}")
            return []
    
    def _clean_text(self, text: str) -> str:
        """Clean text for processing"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\,\/\#\+]', ' ', text)
        
        return text.strip()
    
    def _extract_keyword_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using keyword matching"""
        skills = []
        
        for skill_info in self.all_skills:
            skill = skill_info['skill']
            # Look for exact matches or partial matches
            patterns = [
                r'\b' + re.escape(skill) + r'\b',
                r'\b' + re.escape(skill.replace(' ', r'\s*')) + r'\b'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    skills.append({
                        'name': skill,
                        'category': skill_info['category'],
                        'subcategory': skill_info['subcategory'],
                        'confidence': 0.9,
                        'method': 'keyword',
                        'count': len(matches),
                        'context': self._get_context(text, skill)
                    })
                    break
        
        return skills
    
    def _extract_pattern_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using regex patterns"""
        skills = []
        
        # Common skill patterns
        patterns = {
            'programming_languages': r'\b(python|java|javascript|c\+\+|c\#|ruby|php|swift|kotlin|go|rust|scala|r|matlab)\b',
            'frameworks': r'\b(react|angular|vue|django|flask|spring|express|laravel|rails|node\.js)\b',
            'databases': r'\b(mysql|postgresql|mongodb|redis|sqlite|oracle|sql server|cassandra|elasticsearch)\b',
            'cloud_platforms': r'\b(aws|azure|gcp|google cloud|heroku|digitalocean)\b',
            'tools': r'\b(git|docker|kubernetes|terraform|jenkins|jira|slack|figma|photoshop)\b',
            'certifications': r'\b(aws certified|google certified|pmp|cfa|cpa|itil|prince2)\b',
            'years_experience': r'\b(\d+)\+?\s*(years?|yrs?)\s+(?:of\s+)?(?:experience\s+)?(?:in|with|as)?\s*([a-z\s]+?)(?:\.|,|\s|$)',
        }
        
        for category, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                skill_name = match.group(1) if match.groups() else match.group(0)
                
                # Special handling for years of experience
                if category == 'years_experience' and len(match.groups()) >= 2:
                    years = match.group(1)
                    skill_context = match.group(2).strip()
                    skill_name = f"{skill_context} ({years} years)"
                
                skills.append({
                    'name': skill_name.strip(),
                    'category': 'technical',
                    'subcategory': category,
                    'confidence': 0.8,
                    'method': 'pattern',
                    'count': 1,
                    'context': self._get_context(text, skill_name)
                })
        
        return skills
    
    def _extract_entity_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using NLP entity recognition"""
        skills = []
        
        try:
            self._load_spacy_model()
            if self.nlp is None:
                return skills
            
            doc = self.nlp(text)
            
            # Extract noun phrases that might be skills
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) <= 3 and len(chunk.text) > 2:  # 1-3 words, reasonable length
                    # Check if it matches any known skill
                    for skill_info in self.all_skills:
                        if skill_info['skill'].lower() in chunk.text.lower():
                            skills.append({
                                'name': skill_info['skill'],
                                'category': skill_info['category'],
                                'subcategory': skill_info['subcategory'],
                                'confidence': 0.7,
                                'method': 'entity',
                                'count': 1,
                                'context': chunk.sent.text
                            })
                            break
            
        except Exception as e:
            logger.error(f"Error in entity extraction: {str(e)}")
        
        return skills
    
    def _extract_yake_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using YAKE keyword extraction"""
        skills = []
        
        try:
            # Configure YAKE
            kw_extractor = yake.KeywordExtractor(
                lan="en",
                n=3,  # Max ngram size
                dedupLim=0.7,  # Deduplication threshold
                top=20,  # Number of keywords to return
                features=None
            )
            
            # Extract keywords
            keywords = kw_extractor.extract_keywords(text)
            
            # Filter keywords that match known skills
            for keyword, score in keywords:
                keyword_lower = keyword.lower()
                
                for skill_info in self.all_skills:
                    if skill_info['skill'].lower() in keyword_lower or keyword_lower in skill_info['skill'].lower():
                        skills.append({
                            'name': skill_info['skill'],
                            'category': skill_info['category'],
                            'subcategory': skill_info['subcategory'],
                            'confidence': max(0.5, 1.0 - score),  # Convert YAKE score to confidence
                            'method': 'yake',
                            'count': 1,
                            'context': self._get_context(text, keyword)
                        })
                        break
            
        except Exception as e:
            logger.error(f"Error in YAKE extraction: {str(e)}")
        
        return skills
    
    def _get_context(self, text: str, skill: str, window: int = 50) -> str:
        """Get context around skill mention"""
        try:
            # Find skill in text
            skill_lower = skill.lower()
            text_lower = text.lower()
            
            index = text_lower.find(skill_lower)
            if index == -1:
                return ""
            
            # Extract context window
            start = max(0, index - window)
            end = min(len(text), index + len(skill) + window)
            
            context = text[start:end].strip()
            
            # Clean up context
            context = re.sub(r'\s+', ' ', context)
            
            return context
            
        except Exception:
            return ""
    
    def _deduplicate_skills(self, skills: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate skills and merge information"""
        unique_skills = {}
        
        for skill in skills:
            name = skill['name'].lower().strip()
            
            if name not in unique_skills:
                unique_skills[name] = skill.copy()
            else:
                # Merge information
                existing = unique_skills[name]
                existing['count'] += skill['count']
                existing['confidence'] = max(existing['confidence'], skill['confidence'])
                
                # Combine methods
                if 'methods' not in existing:
                    existing['methods'] = [existing['method']]
                existing['methods'].append(skill['method'])
                existing['methods'] = list(set(existing['methods']))
                existing['method'] = 'combined'
        
        return list(unique_skills.values())
    
    def _rank_skills(self, skills: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """Rank skills by relevance and importance"""
        try:
            # Calculate TF-IDF scores for skills
            skill_names = [skill['name'] for skill in skills]
            
            if len(skill_names) == 0:
                return skills
            
            # Create TF-IDF vectorizer
            vectorizer = TfidfVectorizer(
                vocabulary=skill_names,
                ngram_range=(1, 2),
                stop_words='english'
            )
            
            # Fit and transform
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Add TF-IDF scores to skills
            for i, skill in enumerate(skills):
                skill_name = skill['name']
                if skill_name in feature_names:
                    feature_index = list(feature_names).index(skill_name)
                    skill['tfidf_score'] = tfidf_matrix[0, feature_index]
                else:
                    skill['tfidf_score'] = 0.0
                
                # Calculate final score
                skill['final_score'] = (
                    skill['confidence'] * 0.4 +
                    min(skill['tfidf_score'] * 10, 1.0) * 0.3 +  # Scale TF-IDF
                    min(skill['count'] / 10, 1.0) * 0.3  # Scale count
                )
            
            # Sort by final score
            skills.sort(key=lambda x: x['final_score'], reverse=True)
            
            return skills
            
        except Exception as e:
            logger.error(f"Error ranking skills: {str(e)}")
            # Return original skills if ranking fails
            return skills
    
    def get_skill_statistics(self, skills: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about extracted skills"""
        try:
            if not skills:
                return {
                    'total_skills': 0,
                    'categories': {},
                    'confidence_distribution': {'high': 0, 'medium': 0, 'low': 0},
                    'methods': {}
                }
            
            # Count by category
            categories = Counter(skill['category'] for skill in skills)
            
            # Confidence distribution
            confidence_dist = Counter(
                'high' if skill['confidence'] >= 0.8 else 'medium' if skill['confidence'] >= 0.6 else 'low'
                for skill in skills
            )
            
            # Method distribution
            methods = Counter(skill['method'] for skill in skills)
            
            # Average confidence
            avg_confidence = sum(skill['confidence'] for skill in skills) / len(skills)
            
            # Top skills by score
            top_skills = sorted(skills, key=lambda x: x.get('final_score', 0), reverse=True)[:10]
            
            return {
                'total_skills': len(skills),
                'categories': dict(categories),
                'confidence_distribution': dict(confidence_dist),
                'methods': dict(methods),
                'average_confidence': round(avg_confidence, 2),
                'top_skills': [
                    {
                        'name': skill['name'],
                        'category': skill['category'],
                        'score': round(skill.get('final_score', 0), 2)
                    }
                    for skill in top_skills
                ]
            }
            
        except Exception as e:
            logger.error(f"Error calculating skill statistics: {str(e)}")
            return {}
    
    def suggest_missing_skills(self, skills: List[Dict[str, Any]], target_role: str = None) -> List[str]:
        """Suggest missing skills based on extracted skills and target role"""
        try:
            # Get current skill categories
            current_categories = set(skill['category'] for skill in skills)
            
            # Find underrepresented categories
            missing_categories = []
            for category in self.skill_categories.keys():
                if category not in current_categories:
                    missing_categories.append(category)
            
            suggestions = []
            
            # Suggest skills for missing categories
            for category in missing_categories:
                subcategories = self.skill_categories[category]
                for subcategory, skill_list in subcategories.items():
                    # Suggest top 2 skills from each missing subcategory
                    suggestions.extend(skill_list[:2])
            
            # If target role is specified, add role-specific suggestions
            if target_role:
                role_suggestions = self._get_role_specific_skills(target_role, skills)
                suggestions.extend(role_suggestions)
            
            # Remove duplicates and already present skills
            current_skills = set(skill['name'].lower() for skill in skills)
            unique_suggestions = [
                skill for skill in suggestions 
                if skill.lower() not in current_skills
            ]
            
            return unique_suggestions[:20]  # Return top 20 suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting missing skills: {str(e)}")
            return []
    
    def _get_role_specific_skills(self, role: str, current_skills: List[Dict[str, Any]]) -> List[str]:
        """Get role-specific skill suggestions"""
        role_mappings = {
            'software engineer': ['react', 'node.js', 'python', 'aws', 'docker', 'kubernetes'],
            'data scientist': ['python', 'machine learning', 'tensorflow', 'pandas', 'sql', 'statistics'],
            'product manager': ['product management', 'agile', 'scrum', 'user research', 'analytics', 'stakeholder management'],
            'marketing manager': ['digital marketing', 'seo', 'content marketing', 'analytics', 'social media', 'campaign management'],
            'sales manager': ['business development', 'account management', 'negotiation', 'crm', 'sales strategy', 'client relations']
        }
        
        role_lower = role.lower()
        for mapped_role, skills in role_mappings.items():
            if mapped_role in role_lower:
                current_skill_names = set(skill['name'].lower() for skill in current_skills)
                return [skill for skill in skills if skill.lower() not in current_skill_names]
        
        return []
