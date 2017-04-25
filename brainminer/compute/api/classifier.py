from flask_restful import reqparse
from brainminer.base.api import BaseResource


# ----------------------------------------------------------------------------------------------------------------------
class ClassifiersResource(BaseResource):
    
    URI = '/classifiers'
    
    def get(self):
        return [], 200
    
    def post(self):
        return {}, 201
    
    
# ----------------------------------------------------------------------------------------------------------------------
class ClassifierResource(BaseResource):
    
    URI = '/classifiers/{}'
    
    def get(self, id):
        return {}, 200
    
    def put(self, id):
        return {}, 200
    
    def delete(self, id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionsResource(BaseResource):
    
    URI = '/classifiers/{}/sessions'
    
    def get(self, id):
        return [], 200
    
    def post(self, id):
        return {}, 201
    
    
# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionResource(BaseResource):
    
    URI = '/classifiers/{}/sessions/{}'
    
    def get(self, id, session_id):
        return {}, 200
    
    def put(self, id, session_id):
        return {}, 200
    
    def delete(self, id, session_id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionFilesResource(BaseResource):
    
    URI = '/classifiers/{}/sessions/{}/files/{}'
    
    def put(self, id, session_id, file_id):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionPredictionsResource(BaseResource):
    
    URI = '/classifiers/{}/sessions/{}/predictions'
    
    def get(self, id, session_id):
        return [], 200
    
    def post(self, id, session_id):
        return {}, 201


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionPredictionResource(BaseResource):
    
    URI = '/classifiers/{}/sessions/{}/predictions/{}'
    
    def get(self, id, session_id, prediction_id):
        return {}, 200
    
    def put(self, id, session_id, prediction_id):
        return {}, 200
    
    def delete(self, id, session_id, prediction_id):
        return {}, 204


# ----------------------------------------------------------------------------------------------------------------------
class ClassifierSessionPredictionFilesResource(BaseResource):
    
    URI = '/classifiers/{}/sessions/{}/predictions/{}/files/{}'
    
    def put(self, id, session_id, prediction_id, file_id):
        return {}, 201
