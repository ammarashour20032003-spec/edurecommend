import uuid
from datetime import datetime
from app import db

class Session(db.Model):
    __tablename__ = 'SESSIONS'

    id         = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = db.Column(db.String(36), db.ForeignKey('USERS.id', ondelete='CASCADE'), nullable=False)
    token      = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':         self.id,
            'user_id':    self.user_id,
            'expires_at': str(self.expires_at),
            'created_at': str(self.created_at)
        }