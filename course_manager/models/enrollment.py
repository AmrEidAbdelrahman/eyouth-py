from django.db import models
from django.conf import settings

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_enrolled'
    )
    course = models.ForeignKey("course_manager.Course", on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"

class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey("course_manager.Lesson", on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.student.email} - {self.lesson.title}" 
