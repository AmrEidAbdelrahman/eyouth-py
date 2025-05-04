from django.db import models
from course_manager.models.module import Module

class Lesson(models.Model):
    class ContentType(models.TextChoices):
        VIDEO = 'VIDEO', 'Video'
        PDF = 'PDF', 'PDF'
        TEXT = 'TEXT', 'Text'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=5, choices=ContentType.choices)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to='lesson_pdfs/', null=True, blank=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['module', 'order']

    def __str__(self):
        return f"{self.module.title} - {self.title}" 
    
    @property
    def instructor(self):
        return self.module.course.instructor
