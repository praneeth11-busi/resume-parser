import pdfplumber
from .text_processor import TextProcessor

class PDFParser:
    def __init__(self):
        self.text_processor = TextProcessor()
    
    def parse(self, file_path):
        text = self.extract_text(file_path)
        return self.extract_info(text)
    
    def extract_text(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    
    def extract_info(self, text):
        return {
            'name': self.text_processor.extract_name(text),
            'email': self.text_processor.extract_email(text),
            'phone': self.text_processor.extract_phone(text),
            'skills': self.text_processor.extract_skills(text),
            'experience': self.text_processor.extract_experience(text),
            'education': self.text_processor.extract_education(text),
            'raw_text': text
        }
