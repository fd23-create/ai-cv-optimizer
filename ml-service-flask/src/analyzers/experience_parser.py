import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

class ExperienceParser:
    """Parser for work experience section in resumes"""
    
    def __init__(self):
        # Common section headers
        self.section_headers = [
            'experience', 'work experience', 'professional experience', 'employment',
            'work history', 'career', 'job experience', 'professional background',
            'expériences', 'expérience professionnelle', 'parcours professionnel',
            'emploi', 'travail', 'carrière'
        ]
        
        # Company indicators
        self.company_indicators = [
            'inc', 'corp', 'corporation', 'llc', 'ltd', 'limited', 'co', 'company',
            'group', 'industries', 'technologies', 'solutions', 'services', 'systems'
        ]
        
        # Position indicators
        self.position_keywords = [
            'manager', 'director', 'engineer', 'developer', 'analyst', 'specialist',
            'consultant', 'coordinator', 'administrator', 'assistant', 'associate',
            'lead', 'senior', 'junior', 'principal', 'head', 'chief', 'officer'
        ]
        
        # Date patterns
        self.date_patterns = [
            # Month Year
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b',
            # MM/YYYY
            r'\b(0[1-9]|1[0-2])[/\-](19|20)\d{2}\b',
            # Month YYYY
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b',
            # YYYY
            r'\b(19|20)\d{2}\b',
            # Present/Current
            r'\b(present|current|aujourd\'hui|actuel)\b',
            # French months
            r'\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4}\b'
        ]
        
        # Action verbs for achievements
        self.action_verbs = [
            'managed', 'led', 'developed', 'implemented', 'created', 'designed', 'analyzed',
            'optimized', 'improved', 'increased', 'reduced', 'achieved', 'coordinated', 'trained',
            'mentored', 'collaborated', 'negotiated', 'presented', 'researched', 'evaluated',
            'launched', 'built', 'maintained', 'supported', 'facilitated', 'streamlined'
        ]
    
    def extract_experience(self, text: str, language: str = 'en') -> List[Dict[str, Any]]:
        """
        Extract work experience from resume text
        
        Args:
            text: Resume text
            language: Language code
            
        Returns:
            List of experience entries
        """
        try:
            # Find experience section
            experience_section = self._find_experience_section(text)
            if not experience_section:
                return []
            
            # Split into individual positions
            positions = self._split_positions(experience_section)
            
            # Parse each position
            experiences = []
            for position in positions:
                parsed = self._parse_position(position, language)
                if parsed:
                    experiences.append(parsed)
            
            # Sort by start date (most recent first)
            experiences.sort(key=lambda x: x.get('start_date', ''), reverse=True)
            
            return experiences
            
        except Exception as e:
            logger.error(f"Error extracting experience: {str(e)}")
            return []
    
    def _find_experience_section(self, text: str) -> Optional[str]:
        """Find the experience section in the text"""
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
                'education', 'formation', 'skills', 'compétences', 'summary', 'résumé',
                'profile', 'profil', 'objective', 'objectif', 'projects', 'projets'
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
            logger.error(f"Error finding experience section: {str(e)}")
            return None
    
    def _split_positions(self, section_text: str) -> List[str]:
        """Split experience section into individual positions"""
        try:
            positions = []
            
            # Split by common position separators
            separators = [
                r'\n\s*\n',  # Double newlines
                r'\n[A-Z][a-z]+\s+[A-Z][a-z]+',  # New line with capitalized name
                r'\n\d{4}[-/]\d{1,2}',  # New line with date
                r'\n[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]'  # New line with month
            ]
            
            # Try different splitting strategies
            for separator in separators:
                split_positions = re.split(separator, section_text, flags=re.IGNORECASE | re.MULTILINE)
                
                if len(split_positions) > 1:
                    positions = [pos.strip() for pos in split_positions if pos.strip()]
                    break
            
            # If no good splits found, try bullet point splitting
            if len(positions) <= 1:
                bullet_patterns = [r'•', r'\*', r'-', r'\d+\.', r'\([a-z]\)']
                for pattern in bullet_patterns:
                    split_positions = re.split(f'\n{pattern}\\s*', section_text)
                    if len(split_positions) > 1:
                        positions = [pos.strip() for pos in split_positions if pos.strip()]
                        break
            
            return positions if positions else [section_text]
            
        except Exception as e:
            logger.error(f"Error splitting positions: {str(e)}")
            return [section_text]
    
    def _parse_position(self, position_text: str, language: str = 'en') -> Optional[Dict[str, Any]]:
        """Parse a single position entry"""
        try:
            if not position_text or len(position_text.strip()) < 20:
                return None
            
            # Extract position title and company
            title, company = self._extract_title_and_company(position_text)
            
            # Extract dates
            start_date, end_date, duration = self._extract_dates(position_text)
            
            # Extract location
            location = self._extract_location(position_text)
            
            # Extract description and achievements
            description, achievements = self._extract_description(position_text)
            
            # Calculate metrics
            metrics = self._calculate_metrics(description, achievements)
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'start_date': start_date,
                'end_date': end_date,
                'duration_years': duration,
                'description': description,
                'achievements': achievements,
                'metrics': metrics,
                'is_current': end_date is None or end_date.lower() in ['present', 'current', 'aujourd\'hui'],
                'confidence': self._calculate_confidence(title, company, start_date, description)
            }
            
        except Exception as e:
            logger.error(f"Error parsing position: {str(e)}")
            return None
    
    def _extract_title_and_company(self, text: str) -> Tuple[str, str]:
        """Extract position title and company"""
        try:
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            if not lines:
                return "", ""
            
            title = ""
            company = ""
            
            # First line is usually the title
            first_line = lines[0]
            
            # Check if it looks like a title (contains position keywords)
            if any(keyword.lower() in first_line.lower() for keyword in self.position_keywords):
                title = first_line
                
                # Second line might be company
                if len(lines) > 1:
                    second_line = lines[1]
                    if any(indicator.lower() in second_line.lower() for indicator in self.company_indicators):
                        company = second_line
                    elif not any(keyword.lower() in second_line.lower() for keyword in self.position_keywords):
                        # Likely company if it doesn't contain position keywords
                        company = second_line
            else:
                # Try to find title in first two lines
                for i, line in enumerate(lines[:2]):
                    if any(keyword.lower() in line.lower() for keyword in self.position_keywords):
                        title = line
                        if i == 0 and len(lines) > 1:
                            company = lines[1]
                        elif i == 1:
                            company = lines[0]
                        break
            
            # Clean up
            title = re.sub(r'^[-•\*\d\.\s]+', '', title).strip()
            company = re.sub(r'^[-•\*\d\.\s]+', '', company).strip()
            
            return title, company
            
        except Exception as e:
            logger.error(f"Error extracting title and company: {str(e)}")
            return "", ""
    
    def _extract_dates(self, text: str) -> Tuple[Optional[str], Optional[str], float]:
        """Extract start date, end date, and duration"""
        try:
            # Find all date matches
            date_matches = []
            for pattern in self.date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                date_matches.extend(matches)
            
            if len(date_matches) < 1:
                return None, None, 0.0
            
            # Process dates
            dates = []
            for match in date_matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                
                try:
                    # Parse date
                    if match.lower() in ['present', 'current', 'aujourd\'hui', 'actuel']:
                        dates.append(('present', datetime.now()))
                    else:
                        parsed_date = parse_date(match, fuzzy=True)
                        dates.append((match, parsed_date))
                except:
                    continue
            
            if len(dates) == 0:
                return None, None, 0.0
            
            # Sort dates
            dates.sort(key=lambda x: x[1])
            
            # Extract start and end dates
            start_date_str, start_date = dates[0]
            
            if len(dates) > 1:
                end_date_str, end_date = dates[-1]
            else:
                end_date_str, end_date = 'present', datetime.now()
            
            # Calculate duration
            if end_date and start_date:
                delta = relativedelta(end_date, start_date)
                duration_years = delta.years + delta.months / 12.0
            else:
                duration_years = 0.0
            
            return start_date_str, end_date_str, duration_years
            
        except Exception as e:
            logger.error(f"Error extracting dates: {str(e)}")
            return None, None, 0.0
    
    def _extract_location(self, text: str) -> str:
        """Extract location information"""
        try:
            # Common location patterns
            location_patterns = [
                r',\s*([A-Z][a-z\s]+(?:\s+[A-Z]{2})?)$',  # City, State
                r',\s*([A-Z][a-z\s]+(?:\s+[A-Z]{2})?)\s*\n',  # City, State before newline
                r'([A-Z][a-z\s]+,\s*[A-Z]{2})',  # City, State
                r'([A-Z][a-z\s]+,\s*[A-Z][a-z\s]+)',  # City, Country
                r'(Remote|Télétravail|Remote)',  # Remote work
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
    
    def _extract_description(self, text: str) -> Tuple[str, List[str]]:
        """Extract description and achievements"""
        try:
            # Split into lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            description_lines = []
            achievements = []
            
            # Skip first few lines (likely title, company, dates, location)
            content_lines = lines[3:] if len(lines) > 3 else lines
            
            for line in content_lines:
                # Check if it's an achievement (starts with action verb or bullet point)
                if (re.match(r'^[-•\*\d\.\s]*', line) or 
                    any(verb.lower() in line.lower() for verb in self.action_verbs)):
                    
                    # Clean up achievement
                    achievement = re.sub(r'^[-•\*\d\.\s]+', '', line).strip()
                    if achievement:
                        achievements.append(achievement)
                else:
                    description_lines.append(line)
            
            description = ' '.join(description_lines)
            
            return description, achievements
            
        except Exception as e:
            logger.error(f"Error extracting description: {str(e)}")
            return "", []
    
    def _calculate_metrics(self, description: str, achievements: List[str]) -> Dict[str, Any]:
        """Calculate metrics for the position"""
        try:
            metrics = {
                'quantifiable_achievements': 0,
                'action_verb_count': 0,
                'technical_keywords': 0,
                'management_keywords': 0,
                'achievement_count': len(achievements),
                'description_length': len(description),
                'has_metrics': False
            }
            
            # Check for quantifiable achievements
            quantifiable_patterns = [
                r'\d+%', r'\$\d+', r'\d+\s*(million|billion|thousand|k|m|b)',
                r'\d+\s*(years?|months?)', r'\d+\s*(people|employees|clients|customers)',
                r'\d+\s*(projects|products|services)'
            ]
            
            all_text = description + ' ' + ' '.join(achievements)
            
            for pattern in quantifiable_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                metrics['quantifiable_achievements'] += len(matches)
            
            # Count action verbs
            for verb in self.action_verbs:
                matches = re.findall(rf'\b{re.escape(verb)}\b', all_text, re.IGNORECASE)
                metrics['action_verb_count'] += len(matches)
            
            # Technical keywords
            tech_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 'react', 'node.js']
            for keyword in tech_keywords:
                if keyword.lower() in all_text.lower():
                    metrics['technical_keywords'] += 1
            
            # Management keywords
            mgmt_keywords = ['managed', 'led', 'team', 'project', 'supervised', 'coordinated', 'directed']
            for keyword in mgmt_keywords:
                if keyword.lower() in all_text.lower():
                    metrics['management_keywords'] += 1
            
            metrics['has_metrics'] = metrics['quantifiable_achievements'] > 0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return {}
    
    def _calculate_confidence(self, title: str, company: str, start_date: Optional[str], description: str) -> float:
        """Calculate confidence score for the parsed position"""
        try:
            confidence = 0.0
            
            # Title confidence (40%)
            if title and len(title) > 3:
                if any(keyword.lower() in title.lower() for keyword in self.position_keywords):
                    confidence += 0.4
                else:
                    confidence += 0.2
            
            # Company confidence (20%)
            if company and len(company) > 2:
                if any(indicator.lower() in company.lower() for indicator in self.company_indicators):
                    confidence += 0.2
                else:
                    confidence += 0.1
            
            # Date confidence (20%)
            if start_date:
                confidence += 0.2
            
            # Description confidence (20%)
            if description and len(description) > 20:
                confidence += 0.2
            elif description and len(description) > 10:
                confidence += 0.1
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.0
    
    def get_experience_summary(self, experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics for all experiences"""
        try:
            if not experiences:
                return {
                    'total_positions': 0,
                    'total_experience_years': 0.0,
                    'current_positions': 0,
                    'companies': [],
                    'industries': [],
                    'career_progression': 'unknown'
                }
            
            total_positions = len(experiences)
            total_experience_years = sum(exp.get('duration_years', 0) for exp in experiences)
            current_positions = sum(1 for exp in experiences if exp.get('is_current', False))
            
            companies = list(set(exp.get('company', '') for exp in experiences if exp.get('company')))
            companies = [c for c in companies if c]
            
            # Analyze career progression
            career_progression = self._analyze_career_progression(experiences)
            
            return {
                'total_positions': total_positions,
                'total_experience_years': round(total_experience_years, 1),
                'current_positions': current_positions,
                'companies': companies,
                'company_count': len(companies),
                'career_progression': career_progression,
                'average_position_duration': round(total_experience_years / total_positions, 1) if total_positions > 0 else 0.0
            }
            
        except Exception as e:
            logger.error(f"Error calculating experience summary: {str(e)}")
            return {}
    
    def _analyze_career_progression(self, experiences: List[Dict[str, Any]]) -> str:
        """Analyze career progression pattern"""
        try:
            if len(experiences) < 2:
                return 'insufficient_data'
            
            # Sort by start date
            sorted_experiences = sorted(experiences, key=lambda x: x.get('start_date', ''))
            
            # Check for progression indicators
            progression_indicators = 0
            
            for i in range(len(sorted_experiences) - 1):
                current = sorted_experiences[i]
                next_pos = sorted_experiences[i + 1]
                
                current_title = current.get('title', '').lower()
                next_title = next_pos.get('title', '').lower()
                
                # Check for seniority progression
                seniority_levels = ['junior', 'associate', 'senior', 'lead', 'principal', 'manager', 'director']
                
                current_level = max([seniority_levels.index(level) for level in seniority_levels if level in current_title] or [-1])
                next_level = max([seniority_levels.index(level) for level in seniority_levels if level in next_title] or [-1])
                
                if next_level > current_level:
                    progression_indicators += 1
                
                # Check for responsibility increase
                current_duration = current.get('duration_years', 0)
                next_duration = next_pos.get('duration_years', 0)
                
                if next_duration > current_duration * 1.2:  # 20% increase in duration
                    progression_indicators += 0.5
            
            # Determine progression level
            progression_ratio = progression_indicators / (len(experiences) - 1)
            
            if progression_ratio >= 0.7:
                return 'strong'
            elif progression_ratio >= 0.4:
                return 'moderate'
            elif progression_ratio >= 0.2:
                return 'weak'
            else:
                return 'stagnant'
                
        except Exception as e:
            logger.error(f"Error analyzing career progression: {str(e)}")
            return 'unknown'
