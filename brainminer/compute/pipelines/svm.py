from celery import shared_task
from brainminer.compute.pipelines.base import Pipeline


# ----------------------------------------------------------------------------------------------------------------------
@shared_task
def svm_train(params):
    return {'accuracy': 0.9, 'model_id': 1}


# ----------------------------------------------------------------------------------------------------------------------
@shared_task
def svm(params):
    return {'prediction': 1, 'probability': 0.8}


# ----------------------------------------------------------------------------------------------------------------------
class SupportVectorMachineTrainer(Pipeline):
    
    def run(self, params):
        return svm_train(params)
    
    
# ----------------------------------------------------------------------------------------------------------------------
class SupportVectorMachine(Pipeline):
    
    def run(self, params):
        return svm(params)
