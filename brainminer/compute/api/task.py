from flask_restful import reqparse
from brainminer.base.api import PermissionProtectedResource
from brainminer.compute.worker import run_pipeline


# ----------------------------------------------------------------------------------------------------------------------
class TasksResource(PermissionProtectedResource):
    
    URI = '/tasks'
    
    def post(self):
        
        self.check_permission('create:task')
        parser = reqparse.RequestParser()
        parser.add_argument('pipeline_name', type=str, required=True, location='json')
        parser.add_argument('params', type=dict, required=True, location='json')
        args = parser.parse_args()
        task_id = run_pipeline(**args)
        
        return {'task_id': task_id}, 201
    
    
# ----------------------------------------------------------------------------------------------------------------------
class TaskResource(PermissionProtectedResource):
    
    URI = '/tasks/{}'
    
    def get(self, id):
        return {}, 200
    
    def put(self, id):
        return {}, 200
    
    def delete(self, id):
        return {}, 204
