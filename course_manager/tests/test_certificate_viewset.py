import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models import Certificate, Enrollment, Course

User = get_user_model()

@pytest.mark.django_db
class TestCertificateViewSet:
    
    def test_student_can_view_own_certificates(self, api_client, student, certificate):
        """Test that a student can view their own certificates"""
        # Ensure the certificate belongs to this student
        certificate.enrollment.student = student
        certificate.enrollment.save()
        certificate.refresh_from_db()
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Get certificates
        url = reverse('certificate-list')
        response = api_client.get(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    
    def test_student_cannot_view_other_student_certificates(self, api_client, student, certificate):
        """Test that a student cannot view certificates that belong to other students"""
        # Create another student
        other_student = User.objects.create_user(
            username='other_student',
            email='other_student@example.com',
            password='testpass123',
            first_name='Other',
            last_name='Student',
            role='STUDENT'
        )
        
        # Ensure the certificate belongs to the other student
        certificate.enrollment.student = other_student
        certificate.enrollment.save()
        certificate.refresh_from_db()
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Get certificates
        url = reverse('certificate-list')
        response = api_client.get(url)
        
        # Verify response (should be empty list, not forbidden)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
    
    def test_instructor_can_view_their_course_certificates(self, api_client, instructor, certificate):
        """Test that an instructor can view certificates for their courses"""
        # Ensure the certificate is for a course taught by this instructor
        certificate.enrollment.course.instructor = instructor
        certificate.enrollment.course.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Get certificates
        url = reverse('certificate-list')
        response = api_client.get(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    
    def test_instructor_cannot_view_other_instructor_certificates(self, api_client, instructor, certificate):
        """Test that an instructor cannot view certificates for courses they don't teach"""
        # Create another instructor
        other_instructor = User.objects.create_user(
            username='other_instructor',
            email='other_instructor@example.com',
            password='testpass123',
            first_name='Other',
            last_name='Instructor',
            role='INSTRUCTOR'
        )
        
        # Ensure the certificate is for a course taught by another instructor
        certificate.enrollment.course.instructor = other_instructor
        certificate.enrollment.course.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Get certificates
        url = reverse('certificate-list')
        response = api_client.get(url)
        
        # Verify response (should be empty list, not forbidden)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0
        
    def test_certificate_detail_view(self, api_client, student, certificate):
        """Test that a student can view the details of their certificate"""
        # Ensure the certificate belongs to this student
        certificate.enrollment.student = student
        certificate.enrollment.save()
        certificate.refresh_from_db()
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Get certificate detail
        url = reverse('certificate-detail', kwargs={'pk': certificate.id})
        response = api_client.get(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == certificate.id 
