from celery import Celery
from celery.result import AsyncResult
from brainminer.compute.pipelines.base import PipelineRegistry

celery = Celery('compute')
celery.config_from_object('brainminer.settings')

tasks = []
for key in celery.conf['PIPELINES']:
    tasks.append(celery.conf['PIPELINES'][key]['module_path'])
celery.autodiscover_tasks(tasks)


# ----------------------------------------------------------------------------------------------------------------------
@celery.task(name='run_pipeline')
def run_pipeline(pipeline_name, params):

    registry = PipelineRegistry()
    pipeline = registry.get(pipeline_name)
    task_id = None
    if pipeline is not None:
        task_id = pipeline.run(params)
    else:
        print('Pipeline {} not found'.format(pipeline_name))
        
    return task_id


# ----------------------------------------------------------------------------------------------------------------------
def task_status(task_id):
    result = AsyncResult(task_id)
    return result.status


# ----------------------------------------------------------------------------------------------------------------------
def task_result(task_id):
    result = AsyncResult(task_id)
    return result.result


if __name__ == '__main__':
    celery.worker_main()
