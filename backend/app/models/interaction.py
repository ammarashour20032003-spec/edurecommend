import uuid
from datetime import datetime
from app import db

class Interaction(db.Model):
    __tablename__ = 'INTERACTIONS'

    id               = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id          = db.Column(db.String(36), db.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    content_id       = db.Column(db.String(36), db.ForeignKey('CONTENT.id', ondelete='CASCADE'), nullable=False)
    action           = db.Column(db.Enum('viewed', 'liked', 'rated', 'bookmarked'), nullable=False)
    rating           = db.Column(db.Float)
    duration_seconds = db.Column(db.Integer, default=0)
    interacted_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':               self.id,
            'user_id':          self.user_id,
            'content_id':       self.content_id,
            'action':           self.action,
            'rating':           self.rating,
            'duration_seconds': self.duration_seconds,
            'interacted_at':    str(self.interacted_at)
        }