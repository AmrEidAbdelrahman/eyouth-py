from rest_framework import viewsets, permissions
from course_manager.models.certificate import Certificate
from course_manager.serializers.certificate import CertificateSerializer

class CertificateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'INSTRUCTOR':
            return Certificate.objects.filter(
                enrollment__course__instructor=self.request.user
            )
        return Certificate.objects.filter(
            enrollment__student=self.request.user
        ) 
