import pytest
from django.urls import reverse
from rest_framework import status
from ..models import Course, Enrollment

@pytest.mark.django_db
class TestCourseAPI:
    def test_create_course(self, api_client, instructor):
        api_client.force_authenticate(user=instructor)
        url = reverse('course-list')
        data = {
            'title': 'New Course',
            'description': 'Course Description'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Course.objects.count() == 1
        assert Course.objects.first().instructor == instructor

    def test_list_courses(self, api_client, course, student):
        api_client.force_authenticate(user=student)
        url = reverse('course-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_enroll_course(self, api_client, course, student):
        api_client.force_authenticate(user=student)
        url = reverse('course-enroll', args=[course.id])
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert Enrollment.objects.filter(student=student, course=course).exists() 
