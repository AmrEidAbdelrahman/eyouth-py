import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from course_manager.views.permissions import IsInstructorOrReadOnly, IsInstructor, IsStudent

User = get_user_model()

@pytest.mark.django_db
class TestCustomPermissions:
    
    def test_is_instructor_or_readonly_get(self, student, instructor):
        """Test IsInstructorOrReadOnly allows GET for any authenticated user"""
        permission = IsInstructorOrReadOnly()
        
        # Create factory and request
        factory = APIRequestFactory()
        
        # Test student can perform GET
        request = factory.get('/some-url/')
        request.user = student
        view = APIView()
        
        assert permission.has_permission(request, view) is True
        
        # Test instructor can perform GET
        request = factory.get('/some-url/')
        request.user = instructor
        
        assert permission.has_permission(request, view) is True
    
    def test_is_instructor_or_readonly_post(self, student, instructor):
        """Test IsInstructorOrReadOnly only allows POST for instructors"""
        permission = IsInstructorOrReadOnly()
        
        # Create factory and request
        factory = APIRequestFactory()
        
        # Test student cannot perform POST
        request = factory.post('/some-url/')
        request.user = student
        view = APIView()
        
        assert permission.has_permission(request, view) is False
        
        # Test instructor can perform POST
        request = factory.post('/some-url/')
        request.user = instructor
        
        assert permission.has_permission(request, view) is True
    
    def test_is_instructor_or_readonly_object_permission(self, student, instructor, course):
        """Test IsInstructorOrReadOnly object permission"""
        permission = IsInstructorOrReadOnly()
        
        # Create factory and request
        factory = APIRequestFactory()
        
        # Test student can GET object
        request = factory.get('/some-url/')
        request.user = student
        view = APIView()
        
        assert permission.has_object_permission(request, view, course) is True
        
        # Test student cannot PUT object
        request = factory.put('/some-url/')
        request.user = student
        
        assert permission.has_object_permission(request, view, course) is False
        
        # Test instructor can PUT their own object
        request = factory.put('/some-url/')
        request.user = instructor
        
        # Ensure the instructor owns the course
        course.instructor = instructor
        course.save()
        
        assert permission.has_object_permission(request, view, course) is True
        
        # Test instructor cannot PUT another instructor's object
        another_instructor = User.objects.create_user(
            username='another_instructor',
            email='another@example.com',
            password='testpass123',
            first_name='Another',
            last_name='Instructor',
            role='INSTRUCTOR'
        )
        request.user = another_instructor
        
        assert permission.has_object_permission(request, view, course) is False
    
    def test_is_instructor_permission(self, student, instructor):
        """Test IsInstructor permission"""
        permission = IsInstructor()
        
        # Create factory and request
        factory = APIRequestFactory()
        
        # Test student cannot access
        request = factory.get('/some-url/')
        request.user = student
        view = APIView()
        
        assert permission.has_permission(request, view) is False
        
        # Test instructor can access
        request = factory.get('/some-url/')
        request.user = instructor
        
        assert permission.has_permission(request, view) is True
    
    def test_is_student_permission(self, student, instructor):
        """Test IsStudent permission"""
        permission = IsStudent()
        
        # Create factory and request
        factory = APIRequestFactory()
        
        # Test student can access
        request = factory.get('/some-url/')
        request.user = student
        view = APIView()
        
        assert permission.has_permission(request, view) is True
        
        # Test instructor cannot access
        request = factory.get('/some-url/')
        request.user = instructor
        
        assert permission.has_permission(request, view) is False 
