import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tojet.settings')

# Create a Celery application instance named 'tojet'.
app = Celery('tojet')

# Configure Celery to read settings from Django's settings.py under the 'CELERY' namespace.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks defined in the 'data_collector' app.
app.autodiscover_tasks()

# Set the broker URL for communication between Celery workers (RabbitMQ in this case).
app.conf.broker_url = 'amqp://user:password@rabbitmq:5672//'

# Set the result backend for storing the results of Celery tasks.
app.conf.result_backend = 'rpc://'

# Optional Celery configuration for task processing.
app.conf.update(
    worker_prefetch_multiplier=1,  # Limits the number of tasks each worker can reserve at once.
    timezone="Asia/Tehran",
    enable_utc=True,
    task_track_started=True, # Enable task status tracking to monitor task progress (e.g., PENDING).
    task_acks_late=True,  # Ensures that tasks are acknowledged after they are completed (for reliable task execution).
)

# Store Celery task results in the Django database.
app.conf.result_backend = 'django-db'

# Import the crontab class to configure periodic tasks using cron-like syntax.
# from celery.schedules import crontab

# Define the schedule for periodic tasks.
# app.conf.beat_schedule = {
#     'user_task': {
#         'task': 'user.tasks.example_task',
#         'schedule': crontab(minute='*/4'),
#     },
#
# }
