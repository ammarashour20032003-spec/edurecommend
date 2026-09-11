import uuid
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'USERS'

    id             = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name      = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(150), nullable=False, unique=True)
    password_hash  = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(100))
    level          = db.Column(db.Enum('beginner', 'intermediate', 'advanced'))
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    last_login     = db.Column(db.DateTime)

    # Relationships
    interactions    = db.relationship('Interaction', backref='user', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', lazy=True)
    sessions        = db.relationship('Session', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id':             self.id,
            'full_name':      self.full_name,
            'email':          self.email,
            'specialization': self.specialization,
            'level':          self.level,
            'created_at':     str(self.created_at)
        }