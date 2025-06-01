from celery import Task
from app import app



class flaskContext(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return Task.__call__(self, *args, **kwargs)