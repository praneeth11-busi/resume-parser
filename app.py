import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import Config
from models import db, Candidate, Experience, Education, Skill

# Import parsers
from parser.pdf_parser import PDFParser
from parser.docx_parser import DOCXParser

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    Config.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()

# Initialize parsers
pdf_parser = PDFParser()
docx_parser = DOCXParser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse the resume based on file type
        if filename.endswith('.pdf'):
            parsed_data = pdf_parser.parse(file_path)
        elif filename.endswith('.docx'):
            parsed_data = docx_parser.parse(file_path)
        else:
            flash('Unsupported file type')
            return redirect(request.url)
        
        # Save to database
        candidate = save_to_database(parsed_data)
        
        # Clean up
        os.remove(file_path)
        
        return render_template('results.html', candidate=candidate, parsed_data=parsed_data)
    
    flash('Invalid file type')
    return redirect(request.url)

@app.route('/candidates')
def list_candidates():
    candidates = Candidate.query.all()
    return render_template('candidates.html', candidates=candidates)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        # Search by skill
        skills = Skill.query.filter(Skill.name.ilike(f'%{query}%')).all()
        candidate_ids = [skill.candidate_id for skill in skills]
        
        # Also search by name
        name_matches = Candidate.query.filter(Candidate.name.ilike(f'%{query}%')).all()
        
        # Combine results
        candidates = Candidate.query.filter(
            (Candidate.id.in_(candidate_ids)) | 
            (Candidate.id.in_([c.id for c in name_matches]))
        ).all()
        
        return render_template('candidates.html', candidates=candidates, query=query)
    
    return redirect(url_for('list_candidates'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['pdf', 'docx']

def save_to_database(parsed_data):
    # Check if candidate already exists by email
    if parsed_data['email']:
        candidate = Candidate.query.filter_by(email=parsed_data['email']).first()
    else:
        candidate = None
    
    if not candidate:
        candidate = Candidate(
            name=parsed_data['name'],
            email=parsed_data['email'],
            phone=parsed_data['phone'],
            raw_text=parsed_data['raw_text']
        )
        db.session.add(candidate)
        db.session.flush()  # To get the candidate ID
    
    # Add experiences
    for exp in parsed_data['experience']:
        experience = Experience(
            candidate_id=candidate.id,
            company=exp.get('company', ''),
            position=exp.get('position', ''),
            duration=exp.get('duration', ''),
            description=exp.get('description', '')
        )
        db.session.add(experience)
    
    # Add education
    for edu in parsed_data['education']:
        education = Education(
            candidate_id=candidate.id,
            institution=edu.get('institution', ''),
            degree=edu.get('degree', ''),
            field_of_study=edu.get('field_of_study', ''),
            year=edu.get('year', '')
        )
        db.session.add(education)
    
    # Add skills
    for skill in parsed_data['skills']:
        skill_entry = Skill(
            candidate_id=candidate.id,
            name=skill.get('name', ''),
            category=skill.get('category', '')
        )
        db.session.add(skill_entry)
    
    db.session.commit()
    return candidate

if __name__ == '__main__':
    app.run(debug=True)
