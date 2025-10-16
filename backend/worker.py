from celery import Celery, Task

def make_celery(flask_app):
    class ContextTask(Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['CELERY_BROKER_URL'],
        backend=flask_app.config['CELERY_RESULT_BACKEND']
    )
    celery_app.conf.update(flask_app.config)
    celery_app.Task = ContextTask
    return celery_app
