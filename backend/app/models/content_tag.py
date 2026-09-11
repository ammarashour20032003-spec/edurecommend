from app import db

class ContentTag(db.Model):
    __tablename__ = 'CONTENT_TAGS'

    content_id = db.Column(db.String(36), db.ForeignKey('CONTENT.id', ondelete='CASCADE'), primary_key=True)
    tag_id     = db.Column(db.String(36), db.ForeignKey('TAGS.id', ondelete='CASCADE'), primary_key=True)