from django.db import models
from course_manager.models.enrollment import Enrollment

class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)

    def __str__(self):
        return f"{self.enrollment.student.email} - {self.enrollment.course.title} Certificate" 
