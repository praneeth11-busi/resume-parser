from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    raw_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    experiences = db.relationship('Experience', backref='candidate', lazy='dynamic', cascade='all, delete-orphan')
    educations = db.relationship('Education', backref='candidate', lazy='dynamic', cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='candidate', lazy='dynamic', cascade='all, delete-orphan')

class Experience(db.Model):
    __tablename__ = 'experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    company = db.Column(db.String(200))
    position = db.Column(db.String(200))
    duration = db.Column(db.String(100))
    description = db.Column(db.Text)

class Education(db.Model):
    __tablename__ = 'educations'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    institution = db.Column(db.String(200))
    degree = db.Column(db.String(200))
    field_of_study = db.Column(db.String(200))
    year = db.Column(db.String(50))

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
