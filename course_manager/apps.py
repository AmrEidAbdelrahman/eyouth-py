from django.apps import AppConfig

class CourseManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'course_manager'

    def ready(self):
        import course_manager.signals 
