# Automated Resume Parser

A Flask-based web application that extracts and categorizes information from resumes (PDF/DOCX) and stores them in a searchable database.

## Features

- Extract candidate details (name, email, phone) from resumes
- Identify skills and categorize them
- Parse work experience and education history
- Store extracted information in PostgreSQL database
- Search functionality for candidates by skills or name

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume_parser
Create a virtual environment and activate it:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Download spaCy model:

bash
python -m spacy download en_core_web_sm
Set up PostgreSQL database:

bash
createdb resume_parser
Set environment variables (optional):

bash
export DATABASE_URL=postgresql://username:password@localhost/resume_parser
export SECRET_KEY=your-secret-key
Run the application:

bash
python app.py
