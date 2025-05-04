

from django.db.models.signals import post_save
from django.dispatch import receiver
from course_manager.models.certificate import Certificate
from course_manager.models.enrollment import LessonProgress
from datetime import datetime


@receiver(post_save, sender=LessonProgress)
def on_lesson_progress_save(sender, instance, created, **kwargs):
    """
    This function is called after a LessonProgress object is saved.
    It checks if the progress is 100% and if so, it generate a certificate for the user.
    """
    if created and instance.enrollment.course.get_progress(instance.enrollment.student) == 100:
        instance.enrollment.completed = True
        instance.enrollment.completed_at = datetime.now()
        instance.enrollment.save(update_fields=['completed', 'completed_at'])
        Certificate.objects.create(
            enrollment=instance.enrollment,
        )
