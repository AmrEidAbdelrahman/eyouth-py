from django.db import models
from django.conf import settings

from course_manager.models.enrollment import LessonProgress
from course_manager.models.lesson import Lesson

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_teaching'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)

    def __str__(self):
        return self.title 
    
    def get_progress(self, user):
        lessons = Lesson.objects.filter(module__course=self).count()
        completed_lessons = LessonProgress.objects.filter(enrollment__student=user, lesson__module__course=self).count()
        return completed_lessons / lessons * 100 if lessons > 0 else 0
