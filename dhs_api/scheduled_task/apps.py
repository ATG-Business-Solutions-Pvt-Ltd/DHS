from django.apps import AppConfig


class ScheduledTaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduled_task'

    def ready(self):
        from scheduled_task.scheduler import start
        start()