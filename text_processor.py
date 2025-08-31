import spacy
import re
from dateutil import parser as date_parser
from datetime import datetime

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class TextProcessor:
    def __init__(self):
        self.nlp = nlp
        self.skill_keywords = self._load_skill_keywords()
        
    def _load_skill_keywords(self):
        # This would ideally come from a file or database
        return {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'swift', 'kotlin', 'go', 'rust'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js', 'express'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git', 'ci/cd'],
            'data_science': ['machine learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'data analysis', 'r']
        }
    
    def extract_name(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Unknown"
    
    def extract_email(self, text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def extract_skills(self, text):
        found_skills = []
        text_lower = text.lower()
        
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append({
                        'name': skill,
                        'category': category
                    })
        
        return found_skills
    
    def extract_experience(self, text):
        # Simple regex pattern for experience extraction
        experience_pattern = r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z,]*\s*\d{4})\s*[-–—]\s*(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z,]*\s*\d{4}|Present|Current)'
        experiences = re.findall(experience_pattern, text, re.IGNORECASE)
        
        # Extract company names and positions (simplified approach)
        experience_entries = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(month in line for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
                # Look for company names and positions in nearby lines
                company = self._extract_company(line)
                position = self._extract_position(line)
                
                if company or position:
                    experience_entries.append({
                        'company': company,
                        'position': position,
                        'duration': line.strip()
                    })
        
        return experience_entries
    
    def _extract_company(self, text):
        # Simple approach - look for capitalized words that might be company names
        words = text.split()
        potential_companies = [word for word in words if word.istitle() and len(word) > 2]
        return ' '.join(potential_companies[:2]) if potential_companies else "Unknown Company"
    
    def _extract_position(self, text):
        # Common job titles
        titles = ['developer', 'engineer', 'manager', 'analyst', 'specialist', 'director', 
                 'consultant', 'architect', 'designer', 'administrator']
        
        for title in titles:
            if title.lower() in text.lower():
                return text.split('-')[0].strip() if '-' in text else text.strip()
        
        return "Unknown Position"
    
    def extract_education(self, text):
        education_entries = []
        
        # Look for education keywords
        edu_keywords = ['university', 'college', 'institute', 'bachelor', 'master', 'phd', 'mba', 'degree']
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in edu_keywords):
                education_entries.append({
                    'institution': line.strip(),
                    'degree': self._extract_degree(line),
                    'year': self._extract_education_year(line)
                })
        
        return education_entries
    
    def _extract_degree(self, text):
        degrees = ['bachelor', 'master', 'phd', 'mba', 'associate', 'diploma', 'certificate']
        for degree in degrees:
            if degree in text.lower():
                return degree.capitalize()
        return "Degree"
    
    def _extract_education_year(self, text):
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        return years[0] if years else "Unknown"
