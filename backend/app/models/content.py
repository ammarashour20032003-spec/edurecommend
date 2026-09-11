import uuid
from datetime import datetime
from app import db

class Content(db.Model):
    __tablename__ = 'CONTENT'

    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title      = db.Column(db.String(255), nullable=False)
    type       = db.Column(db.Enum('article', 'course', 'video'), nullable=False)
    url        = db.Column(db.Text, nullable=False)
    field      = db.Column(db.String(100))
    level      = db.Column(db.Enum('beginner', 'intermediate', 'advanced'))
    avg_rating = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    interactions    = db.relationship('Interaction', backref='content', lazy=True)
    recommendations = db.relationship('Recommendation', backref='content', lazy=True)
    tags            = db.relationship('ContentTag', backref='content', lazy=True)

    def to_dict(self):
        return {
            'id':         self.id,
            'title':      self.title,
            'type':       self.type,
            'url':        self.url,
            'field':      self.field,
            'level':      self.level,
            'avg_rating': self.avg_rating,
            'created_at': str(self.created_at)
        }