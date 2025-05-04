from datetime import datetime, timezone
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ..models import Course, Module, Lesson, Certificate, Enrollment

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def instructor():
    return User.objects.create_user(
        username='instructor',
        email='instructor@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Instructor',
        role='INSTRUCTOR'
    )

@pytest.fixture
def student():
    return User.objects.create_user(
        username='student',
        email='student@example.com',
        password='testpass123',
        first_name='Test',
        last_name='Student',
        role='STUDENT'
    )

@pytest.fixture
def course(instructor):
    return Course.objects.create(
        title='Test Course',
        description='Test Description',
        instructor=instructor,
        is_published=True
    )

@pytest.fixture
def module(course):
    return Module.objects.create(
        course=course,
        title='Test Module',
        order=1
    )

@pytest.fixture
def lesson(module):
    return Lesson.objects.create(
        module=module,
        title='Test Lesson',
        content_type='TEXT',
        content='Test Content',
        order=1
    )

@pytest.fixture
def enrollment(course, student):
    return Enrollment.objects.create(
        student=student,
        course=course
    )

@pytest.fixture
def certificate(enrollment):
    enrollment.completed = True
    enrollment.completed_at = datetime.now()
    enrollment.save()
    return Certificate.objects.create(
        enrollment=enrollment
    ) 
