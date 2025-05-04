import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from course_manager.models import Module

User = get_user_model()

@pytest.mark.django_db
class TestModuleAPI:
    
    def test_instructor_can_create_module(self, api_client, instructor, course):
        """Test that an instructor can create a module for their own course"""
        # Set the course instructor
        course.instructor = instructor
        course.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Create a module
        url = reverse('module-list')
        data = {
            'course': course.id,
            'title': 'Test Module',
            'order': 1
        }
        response = api_client.post(url, data)
        
        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Module'
        assert Module.objects.count() == 1
    
    def test_instructor_cannot_create_module_for_other_course(self, api_client, instructor, course):
        """Test that an instructor cannot create a module for another instructor's course"""
        # Create another instructor who owns the course
        other_instructor = User.objects.create_user(
            username='other_instructor',
            email='other_instructor@example.com',
            password='testpass123',
            first_name='Other',
            last_name='Instructor',
            role='INSTRUCTOR'
        )
        course.instructor = other_instructor
        course.save()
        
        # Authenticate as instructor who doesn't own the course
        api_client.force_authenticate(user=instructor)
        
        # Attempt to create a module
        url = reverse('module-list')
        data = {
            'course': course.id,
            'title': 'Test Module',
            'order': 1
        }
        response = api_client.post(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Module.objects.count() == 0
    
    def test_student_cannot_create_module(self, api_client, student, course):
        """Test that a student cannot create a module"""
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to create a module
        url = reverse('module-list')
        data = {
            'course': course.id,
            'title': 'Test Module',
            'order': 1
        }
        response = api_client.post(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Module.objects.count() == 0
    
    def test_instructor_can_update_own_module(self, api_client, instructor, course, module):
        """Test that an instructor can update their own module"""
        # Set the course instructor to match the module's course
        course.instructor = instructor
        course.save()
        module.course = course
        module.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Update the module
        url = reverse('module-detail', args=[module.id])
        data = {
            'title': 'Updated Module Title',
            'order': 2
        }
        response = api_client.patch(url, data)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Module Title'
        assert response.data['order'] == 2
    
    def test_instructor_cannot_update_other_module(self, api_client, instructor, course, module):
        """Test that an instructor cannot update another instructor's module"""
        # Create another instructor who owns the course/module
        other_instructor = User.objects.create_user(
            username='other_instructor',
            email='other_instructor@example.com',
            password='testpass123',
            first_name='Other',
            last_name='Instructor',
            role='INSTRUCTOR'
        )
        course.instructor = other_instructor
        course.save()
        module.course = course
        module.save()
        
        # Authenticate as different instructor
        api_client.force_authenticate(user=instructor)
        
        # Attempt to update the module
        url = reverse('module-detail', args=[module.id])
        data = {
            'title': 'Should Not Update',
            'order': 99
        }
        response = api_client.patch(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify module was not updated
        module.refresh_from_db()
        assert module.title != 'Should Not Update'
    
    def test_student_cannot_update_module(self, api_client, student, module):
        """Test that a student cannot update a module"""
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to update the module
        url = reverse('module-detail', args=[module.id])
        data = {
            'title': 'Should Not Update',
            'order': 99
        }
        response = api_client.patch(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify module was not updated
        module.refresh_from_db()
        assert module.title != 'Should Not Update'
    
    def test_instructor_can_delete_own_module(self, api_client, instructor, course, module):
        """Test that an instructor can delete their own module"""
        # Set the course instructor to match the module's course
        course.instructor = instructor
        course.save()
        module.course = course
        module.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Delete the module
        url = reverse('module-detail', args=[module.id])
        response = api_client.delete(url)
        
        # Verify response
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify module was deleted
        assert not Module.objects.filter(id=module.id).exists()
    
    def test_instructor_cannot_delete_other_module(self, api_client, instructor, course, module):
        """Test that an instructor cannot delete another instructor's module"""
        # Create another instructor who owns the course/module
        other_instructor = User.objects.create_user(
            username='other_instructor',
            email='other_instructor@example.com',
            password='testpass123',
            first_name='Other',
            last_name='Instructor',
            role='INSTRUCTOR'
        )
        course.instructor = other_instructor
        course.save()
        module.course = course
        module.save()
        
        # Authenticate as different instructor
        api_client.force_authenticate(user=instructor)
        
        # Attempt to delete the module
        url = reverse('module-detail', args=[module.id])
        response = api_client.delete(url)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify module was not deleted
        assert Module.objects.filter(id=module.id).exists()
    
    def test_student_cannot_delete_module(self, api_client, student, module):
        """Test that a student cannot delete a module"""
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to delete the module
        url = reverse('module-detail', args=[module.id])
        response = api_client.delete(url)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify module was not deleted
        assert Module.objects.filter(id=module.id).exists()
    

    
    def test_instructor_can_view_own_course_modules(self, api_client, instructor, course, module):
        """Test that an instructor can view modules for their own course, even if unpublished"""
        # Make sure course is not published and belongs to instructor
        course.is_published = False
        course.instructor = instructor
        course.save()
        module.course = course
        module.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # View course modules
        url = reverse('module-list') + f'?course={course.id}'
        response = api_client.get(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['id'] == module.id 
