import uuid
from datetime import datetime
from app import db

class Recommendation(db.Model):
    __tablename__ = 'RECOMMENDATIONS'

    id           = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id      = db.Column(db.String(36), db.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    content_id   = db.Column(db.String(36), db.ForeignKey('CONTENT.id', ondelete='CASCADE'), nullable=False)
    score        = db.Column(db.Float, nullable=False)
    algorithm    = db.Column(db.String(60), nullable=False)
    clicked      = db.Column(db.Boolean, default=False)
    saved        = db.Column(db.Boolean, default=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'user_id':      self.user_id,
            'content_id':   self.content_id,
            'score':        self.score,
            'algorithm':    self.algorithm,
            'clicked':      self.clicked,
            'saved':        self.saved,
            'generated_at': str(self.generated_at)
        }