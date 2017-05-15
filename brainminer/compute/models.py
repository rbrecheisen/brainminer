from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from brainminer.base.models import BaseModel


# ----------------------------------------------------------------------------------------------------------------------
class Classifier(BaseModel):

    __tablename__ = 'classifier'
    __mapper_args__ = {
        'polymorphic_identity': 'classifier',
    }

    # Classifier ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # External ID
    external_id = Column(String, nullable=False, unique=True)
    # Classifier name
    name = Column(String, nullable=False, unique=True)
        
    def to_dict(self):
        sessions = []
        for session in self.sessions:
            sessions.append(session.to_dict())
        obj = super(Classifier, self).to_dict()
        obj.update({
            'name': self.name,
            'external_id': self.external_id,
            'sessions': sessions,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class Session(BaseModel):

    __tablename__ = 'session'
    __mapper_args__ = {
        'polymorphic_identity': 'session',
    }

    # Session ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Training file path
    training_file_path = Column(String)
    # Classifier object file path
    classifier_file_path = Column(String)
    # Session classifier
    classifier_id = Column(Integer, ForeignKey('classifier.id'), nullable=False)
    classifier = relationship('Classifier', backref='sessions', foreign_keys=[classifier_id])

    def to_dict(self):
        obj = super(Session, self).to_dict()
        obj.update({
            'training_file_path': self.training_file_path,
            'classifier_file_path': self.classifier_file_path,
        })
        return obj