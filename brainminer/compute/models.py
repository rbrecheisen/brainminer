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
    # Classifier name
    name = Column(String(255), nullable=False, unique=True)
        
    def to_dict(self):
        sessions = []
        for session in self.sessions:
            sessions.append(session.to_dict())
        obj = super(Classifier, self).to_dict()
        obj.update({
            'name': self.name,
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
    # Classifier object file path
    object_file_path = Column(String)
    # Session classifier
    classifier_id = Column(Integer, ForeignKey('classifier.id'), nullable=False)
    classifier = relationship('Classifier', backref='sessions', foreign_keys=[classifier_id])

    def to_dict(self):
        predictions = []
        for prediction in self.predictions:
            predictions.append(prediction.to_dict())
        obj = super(Session, self).to_dict()
        obj.update({
            'predictions': predictions,
            'object_file_path': self.object_file_path,
        })
        return obj


# ----------------------------------------------------------------------------------------------------------------------
class Prediction(BaseModel):
    
    __tablename__ = 'prediction'
    __mapper_args__ = {
        'polymorphic_identity': 'prediction',
    }

    # Prediction ID in database
    id = Column(Integer, ForeignKey('base.id'), primary_key=True)
    # Session instance
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    session = relationship('Session', backref='predictions', foreign_keys=[session_id])
    
    def to_dict(self):
        obj = super(Prediction, self).to_dict()
        return obj
