import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class EducationParser:
    """Parser for education section in resumes"""
    
    def __init__(self):
        # Section headers
        self.section_headers = [
            'education', 'academic', 'formation', 'éducation', 'académique',
            'academic background', 'educational background', 'qualifications',
            'diplôme', 'études', 'cursus', 'parcours académique'
        ]
        
        # Degree levels with hierarchy
        self.degree_levels = {
            'high_school': 1,
            'associate': 2,
            'bachelor': 3,
            'licence': 3,  # French equivalent
            'master': 4,
            'master\'s': 4,
            'mba': 4.5,
            'phd': 5,
            'doctorate': 5,
            'doctorat': 5,  # French equivalent
            'postdoc': 6
        }
        
        # Degree keywords
        self.degree_keywords = {
            'high_school': ['high school', 'secondary school', 'lycée', 'baccalauréat', 'bac', 'gcses', 'a-levels'],
            'associate': ['associate', 'associates', 'associate degree', 'dut', 'bts'],
            'bachelor': ['bachelor', 'bachelors', 'bachelor\'s', 'ba', 'bs', 'b.sc', 'b.a', 'b.s', 'licence', 'license'],
            'master': ['master', 'masters', 'master\'s', 'ma', 'ms', 'm.sc', 'm.a', 'm.s', 'mastère'],
            'mba': ['mba', 'master of business administration'],
            'phd': ['phd', 'ph.d', 'doctorate', 'doctor', 'doctoral', 'ph.d.', 'doctorat'],
            'postdoc': ['postdoc', 'post-doctoral', 'postdoctoral']
        }
        
        # Field of study keywords
        self.field_keywords = {
            'computer_science': ['computer science', 'computer engineering', 'software engineering', 'information technology', 'it'],
            'business': ['business', 'business administration', 'management', 'finance', 'marketing', 'accounting'],
            'engineering': ['engineering', 'mechanical engineering', 'electrical engineering', 'civil engineering', 'chemical engineering'],
            'science': ['science', 'biology', 'chemistry', 'physics', 'mathematics', 'statistics'],
            'arts': ['arts', 'literature', 'history', 'philosophy', 'languages', 'communication'],
            'medicine': ['medicine', 'medical', 'nursing', 'pharmacy', 'healthcare', 'public health'],
            'law': ['law', 'legal', 'juris', 'jurisprudence', 'droit'],
            'education': ['education', 'teaching', 'pedagogy', 'pédagogie']
        }
        
        # Institution types
        self.institution_types = [
            'university', 'college', 'institute', 'school', 'academy', 'conservatory',
            'université', 'école', 'institut', 'conservatoire'
        ]
        
        # Date patterns
        self.date_patterns = [
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',
            r'\b(0[1-9]|1[0-2])[/\-](19|20)\d{2}\b',
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b',
            r'\b(19|20)\d{2}\b',
            r'\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b'
        ]
        
        # Achievement indicators
        self.achievement_indicators = [
            'cum laude', 'magna cum laude', 'summa cum laude', 'honors', 'distinction',
            'gpa', 'grade point average', 'dean\'s list', 'scholarship', 'award',
            'mention bien', 'mention très bien', 'distinction', 'prix'
        ]
    
    def extract_education(self, text: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Extract education information from resume text
        
        Args:
            text: Resume text
            language: Language code
            
        Returns:
            List of education entries
        """
        try:
            # Find education section
            education_section = self._find_education_section(text)
            if not education_section:
                return []
            
            # Split into individual entries
            entries = self._split_education_entries(education_section)
            
            # Parse each entry
            education_list = []
            for entry in entries:
                parsed = self._parse_education_entry(entry, language)
                if parsed:
                    education_list.append(parsed)
            
            # Sort by degree level (highest first)
            education_list.sort(key=lambda x: x.get('level_score', 0), reverse=True)
            
            return education_list
            
        except Exception as e:
            logger.error(f"Error extracting education: {str(e)}")
            return []
    
    def _find_education_section(self, text: str) -> Optional[str]:
        """Find the education section in the text"""
        try:
            text_lower = text.lower()
            
            # Find section header
            header_index = None
            for header in self.section_headers:
                index = text_lower.find(header)
                if index != -1:
                    header_index = index
                    break
            
            if header_index is None:
                return None
            
            # Find next section header to determine boundaries
            next_section_headers = [
                'experience', 'expériences', 'work', 'skills', 'compétences',
                'summary', 'résumé', 'profile', 'profil', 'projects', 'projets'
            ]
            
            section_start = header_index
            section_end = len(text)
            
            # Look for next section
            text_after_header = text[header_index + len(self.section_headers[0]):].lower()
            
            for next_header in next_section_headers:
                index = text_after_header.find(next_header)
                if index != -1:
                    section_end = header_index + len(self.section_headers[0]) + index
                    break
            
            return text[section_start:section_end].strip()
            
        except Exception as e:
            logger.error(f"Error finding education section: {str(e)}")
            return None
    
    def _split_education_entries(self, section_text: str) -> List[str]:
        """Split education section into individual entries"""
        try:
            entries = []
            
            # Split by common separators
            separators = [
                r'\n\s*\n',  # Double newlines
                r'\n[A-Z][a-z]+\s+(University|College|Institute|School|École|Université|Institut)',  # New institution
                r'\n\d{4}[-/]\d{1,2}',  # New line with date
                r'\nBachelor|Master|PhD|Licence|Master|Doctorat'  # New degree
            ]
            
            # Try different splitting strategies
            for separator in separators:
                split_entries = re.split(separator, section_text, flags=re.IGNORECASE | re.MULTILINE)
                
                if len(split_entries) > 1:
                    entries = [entry.strip() for entry in split_entries if entry.strip()]
                    break
            
            # If no good splits found, try bullet point splitting
            if len(entries) <= 1:
                bullet_patterns = [r'•', r'\*', r'-', r'\d+\.', r'\([a-z]\)']
                for pattern in bullet_patterns:
                    split_entries = re.split(f'\n{pattern}\\s*', section_text)
                    if len(split_entries) > 1:
                        entries = [entry.strip() for entry in split_entries if entry.strip()]
                        break
            
            return entries if entries else [section_text]
            
        except Exception as e:
            logger.error(f"Error splitting education entries: {str(e)}")
            return [section_text]
    
    def _parse_education_entry(self, entry_text: str, language: str = 'en') -> Optional[Dict[str, Any]]:
        """Parse a single education entry"""
        try:
            if not entry_text or len(entry_text.strip()) < 15:
                return None
            
            # Extract degree and field
            degree, field = self._extract_degree_and_field(entry_text)
            
            # Extract institution
            institution = self._extract_institution(entry_text)
            
            # Extract dates
            start_date, end_date = self._extract_education_dates(entry_text)
            
            # Extract location
            location = self._extract_location(entry_text)
            
            # Extract achievements and GPA
            achievements, gpa = self._extract_achievements(entry_text)
            
            # Calculate level score
            level_score = self._calculate_level_score(degree)
            
            return {
                'degree': degree,
                'field': field,
                'institution': institution,
                'location': location,
                'start_date': start_date,
                'end_date': end_date,
                'gpa': gpa,
                'achievements': achievements,
                'level_score': level_score,
                'is_current': end_date is None or 'present' in end_date.lower(),
                'confidence': self._calculate_confidence(degree, institution, start_date)
            }
            
        except Exception as e:
            logger.error(f"Error parsing education entry: {str(e)}")
            return None
    
    def _extract_degree_and_field(self, text: str) -> Tuple[str, str]:
        """Extract degree and field of study"""
        try:
            degree = ""
            field = ""
            
            text_lower = text.lower()
            
            # Find degree
            for degree_level, keywords in self.degree_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        degree = keyword
                        break
                if degree:
                    break
            
            # Find field of study
            for field_category, keywords in self.field_keywords.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        field = keyword
                        break
                if field:
                    break
            
            # Look for "in" or "of" patterns for field extraction
            if not field:
                field_patterns = [
                    r'(?:bachelor|master|phd|degree|diplôme)[^,]*\b(?:in|of|en|de)\s+([a-z\s]+?)(?:[,\.]|$)',
                    r'(?:bachelor|master|phd)[^,]*\b(?:in|of|en|de)\s+([a-z\s]+?)(?:[,\.]|$)'
                ]
                
                for pattern in field_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        field = match.group(1).strip()
                        break
            
            # Clean up results
            degree = re.sub(r'^[-•\*\d\.\s]+', '', degree).strip()
            field = re.sub(r'^[-•\*\d\.\s]+', '', field).strip()
            
            return degree, field
            
        except Exception as e:
            logger.error(f"Error extracting degree and field: {str(e)}")
            return "", ""
    
    def _extract_institution(self, text: str) -> str:
        """Extract institution name"""
        try:
            # Look for institution type indicators
            institution_patterns = [
                r'\b([A-Z][a-z\s]+(?:University|College|Institute|School|Academy)[A-Za-z\s]*)',
                r'\b([A-Z][a-z\s]+(?:Université|École|Institut|Conservatoire)[A-Za-z\s]*)',
                r'\b([A-Z][a-z\s]+(?:U|I|S|C|E)[A-Z][a-z\s]*)'  # Abbreviations
            ]
            
            for pattern in institution_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    institution = match.group(1).strip()
                    # Clean up
                    institution = re.sub(r'\s+', ' ', institution)
                    return institution
            
            # If no pattern matches, try to extract capitalized phrases
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            for line in lines:
                # Skip lines that are clearly dates or achievements
                if any(indicator.lower() in line.lower() for indicator in ['gpa', 'cum laude', 'honor', 'mention']):
                    continue
                
                # Look for capitalized phrases
                words = line.split()
                capitalized_words = [word for word in words if word[0].isupper() and len(word) > 2]
                
                if len(capitalized_words) >= 2 and any(inst_type.lower() in line.lower() for inst_type in self.institution_types):
                    return line.strip()
            
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting institution: {str(e)}")
            return ""
    
    def _extract_education_dates(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract education dates"""
        try:
            # Find all date matches
            date_matches = []
            for pattern in self.date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                date_matches.extend(matches)
            
            if len(date_matches) < 1:
                return None, None
            
            # Process dates
            dates = []
            for match in date_matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                
                try:
                    # Basic date validation
                    if re.search(r'(19|20)\d{2}', match):
                        dates.append(match)
                except:
                    continue
            
            if len(dates) == 0:
                return None, None
            
            # Return first date as start date, last as end date
            start_date = dates[0]
            end_date = dates[-1] if len(dates) > 1 else None
            
            return start_date, end_date
            
        except Exception as e:
            logger.error(f"Error extracting education dates: {str(e)}")
            return None, None
    
    def _extract_location(self, text: str) -> str:
        """Extract location information"""
        try:
            # Common location patterns
            location_patterns = [
                r',\s*([A-Z][a-z\s]+(?:\s+[A-Z]{2})?)$',  # City, State
                r',\s*([A-Z][a-z\s]+(?:\s+[A-Z]{2})?)\s*\n',  # City, State before newline
                r'([A-Z][a-z\s]+,\s*[A-Z]{2})',  # City, State
                r'([A-Z][a-z\s]+,\s*[A-Z][a-z\s]+)',  # City, Country
                r'\b([A-Z][a-z\s]+)\s*,\s*[A-Z][a-z\s]+\b'  # General pattern
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    # Clean up location
                    location = re.sub(r'\s+', ' ', location)
                    return location
            
            return ""
            
        except Exception as e:
            logger.error(f"Error extracting location: {str(e)}")
            return ""
    
    def _extract_achievements(self, text: str) -> Tuple[List[str], Optional[float]]:
        """Extract achievements and GPA"""
        try:
            achievements = []
            gpa = None
            
            text_lower = text.lower()
            
            # Extract achievements
            for indicator in self.achievement_indicators:
                if indicator in text_lower:
                    # Find the full achievement phrase
                    pattern = rf'([^\.]*{re.escape(indicator)}[^\.]*)'
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    for match in matches:
                        achievement = match.strip()
                        if len(achievement) > 5:
                            achievements.append(achievement)
            
            # Extract GPA
            gpa_patterns = [
                r'gpa[:\s]*([0-3]\.[0-9]|[4]\.0)',
                r'grade point average[:\s]*([0-3]\.[0-9]|[4]\.0)',
                r'average[:\s]*([0-3]\.[0-9]|[4]\.0)'
            ]
            
            for pattern in gpa_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        gpa = float(match.group(1))
                        break
                    except ValueError:
                        continue
            
            return achievements, gpa
            
        except Exception as e:
            logger.error(f"Error extracting achievements: {str(e)}")
            return [], None
    
    def _calculate_level_score(self, degree: str) -> float:
        """Calculate education level score"""
        try:
            if not degree:
                return 0.0
            
            degree_lower = degree.lower()
            
            for level, score in self.degree_levels.items():
                for keyword in self.degree_keywords.get(level, []):
                    if keyword in degree_lower:
                        return score
            
            # Default score for unrecognized degrees
            return 2.0
            
        except Exception as e:
            logger.error(f"Error calculating level score: {str(e)}")
            return 0.0
    
    def _calculate_confidence(self, degree: str, institution: str, start_date: Optional[str]) -> float:
        """Calculate confidence score for the parsed education entry"""
        try:
            confidence = 0.0
            
            # Degree confidence (40%)
            if degree and len(degree) > 2:
                if any(keyword in degree.lower() for keywords in self.degree_keywords.values() for keyword in keywords):
                    confidence += 0.4
                else:
                    confidence += 0.2
            
            # Institution confidence (30%)
            if institution and len(institution) > 3:
                if any(inst_type.lower() in institution.lower() for inst_type in self.institution_types):
                    confidence += 0.3
                else:
                    confidence += 0.15
            
            # Date confidence (20%)
            if start_date:
                confidence += 0.2
            
            # Length confidence (10%)
            if len(degree) + len(institution) > 10:
                confidence += 0.1
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.0
    
    def get_education_summary(self, education_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics for all education entries"""
        try:
            if not education_list:
                return {
                    'total_education': 0,
                    'highest_level': 'none',
                    'institutions': [],
                    'fields': [],
                    'has_gpa': False,
                    'average_gpa': 0.0
                }
            
            total_education = len(education_list)
            
            # Find highest level
            highest_level_entry = max(education_list, key=lambda x: x.get('level_score', 0))
            highest_level = self._get_level_name(highest_level_entry.get('level_score', 0))
            
            # Collect institutions and fields
            institutions = list(set(edu.get('institution', '') for edu in education_list if edu.get('institution')))
            institutions = [inst for inst in institutions if inst]
            
            fields = list(set(edu.get('field', '') for edu in education_list if edu.get('field')))
            fields = [field for field in fields if field]
            
            # GPA information
            gpa_list = [edu.get('gpa') for edu in education_list if edu.get('gpa') is not None]
            has_gpa = len(gpa_list) > 0
            average_gpa = sum(gpa_list) / len(gpa_list) if gpa_list else 0.0
            
            return {
                'total_education': total_education,
                'highest_level': highest_level,
                'highest_level_score': highest_level_entry.get('level_score', 0),
                'institutions': institutions,
                'institution_count': len(institutions),
                'fields': fields,
                'field_count': len(fields),
                'has_gpa': has_gpa,
                'average_gpa': round(average_gpa, 2),
                'achievements_count': sum(len(edu.get('achievements', [])) for edu in education_list)
            }
            
        except Exception as e:
            logger.error(f"Error calculating education summary: {str(e)}")
            return {}
    
    def _get_level_name(self, score: float) -> str:
        """Get level name from score"""
        try:
            for level, level_score in self.degree_levels.items():
                if abs(score - level_score) < 0.1:
                    return level.replace('_', ' ').title()
            
            return 'Unknown'
            
        except Exception:
            return 'Unknown'
    
    def assess_education_relevance(self, education_list: List[Dict[str, Any]], target_field: str = None) -> Dict[str, Any]:
        """Assess relevance of education to target field"""
        try:
            if not education_list:
                return {
                    'relevance_score': 0.0,
                    'relevant_degrees': [],
                    'field_match': False,
                    'recommendations': []
                }
            
            relevance_score = 0.0
            relevant_degrees = []
            field_match = False
            
            # Check field relevance
            if target_field:
                target_lower = target_field.lower()
                for edu in education_list:
                    edu_field = edu.get('field', '').lower()
                    if target_lower in edu_field or edu_field in target_lower:
                        relevance_score += 30
                        field_match = True
                        relevant_degrees.append(edu.get('degree', ''))
            
            # Check degree level relevance
            highest_score = max(edu.get('level_score', 0) for edu in education_list)
            if highest_score >= 4:  # Master's or above
                relevance_score += 25
            elif highest_score >= 3:  # Bachelor's
                relevance_score += 15
            
            # Check institution quality (simplified)
            top_institutions = ['university', 'college', 'institute', 'université', 'école']
            for edu in education_list:
                institution = edu.get('institution', '').lower()
                if any(top_inst in institution for top_inst in top_institutions):
                    relevance_score += 10
                    break
            
            # Check achievements
            total_achievements = sum(len(edu.get('achievements', [])) for edu in education_list)
            if total_achievements > 0:
                relevance_score += min(total_achievements * 2, 15)
            
            # Check GPA
            gpa_list = [edu.get('gpa') for edu in education_list if edu.get('gpa') is not None]
            if gpa_list:
                avg_gpa = sum(gpa_list) / len(gpa_list)
                if avg_gpa >= 3.5:
                    relevance_score += 10
                elif avg_gpa >= 3.0:
                    relevance_score += 5
            
            # Generate recommendations
            recommendations = []
            if relevance_score < 40:
                recommendations.append("Consider highlighting relevant coursework or projects")
            if not field_match and target_field:
                recommendations.append(f"Consider emphasizing transferable skills relevant to {target_field}")
            if highest_score < 3:
                recommendations.append("Consider pursuing additional education or certifications")
            
            return {
                'relevance_score': min(relevance_score, 100),
                'relevant_degrees': relevant_degrees,
                'field_match': field_match,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error assessing education relevance: {str(e)}")
            return {
                'relevance_score': 0.0,
                'relevant_degrees': [],
                'field_match': False,
                'recommendations': []
            }
