import uuid
from app import db

class Tag(db.Model):
    __tablename__ = 'TAGS'

    id   = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False, unique=True)

    # Relationships
    content_tags = db.relationship('ContentTag', backref='tag', lazy=True)

    def to_dict(self):
        return {
            'id':   self.id,
            'name': self.name
        }