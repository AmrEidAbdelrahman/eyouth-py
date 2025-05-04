import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from course_manager.models import Lesson, LessonProgress

User = get_user_model()

@pytest.mark.django_db
class TestLessonAPI:
    
    def test_instructor_can_create_lesson(self, api_client, instructor, course, module):
        """Test that an instructor can create a lesson for their own module"""
        # Set the course instructor
        course.instructor = instructor
        course.save()
        module.course = course
        module.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Create a lesson
        url = reverse('lesson-list')
        data = {
            'module': module.id,
            'title': 'Test Lesson',
            'content_type': 'TEXT',
            'content': 'Test content for the lesson',
            'order': 1
        }
        response = api_client.post(url, data)
        
        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Lesson'
        assert Lesson.objects.count() == 1
    
    def test_instructor_cannot_create_lesson_for_other_module(self, api_client, instructor, course, module):
        """Test that an instructor cannot create a lesson for another instructor's module"""
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
        
        # Attempt to create a lesson
        url = reverse('module-add-lesson', kwargs={'pk': module.id})
        data = {
            'title': 'Test Lesson',
            'content_type': 'TEXT',
            'content': 'Test content for the lesson',
            'order': 1
        }
        response = api_client.post(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Lesson.objects.count() == 0
    
    def test_student_cannot_create_lesson(self, api_client, student, module):
        """Test that a student cannot create a lesson"""
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to create a lesson
        url = reverse('lesson-list')
        data = {
            'module': module.id,
            'title': 'Test Lesson',
            'content_type': 'TEXT',
            'content': 'Test content for the lesson',
            'order': 1
        }
        response = api_client.post(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Lesson.objects.count() == 0
    
    def test_instructor_can_update_own_lesson(self, api_client, instructor, course, module, lesson):
        """Test that an instructor can update their own lesson"""
        # Set the course instructor
        course.instructor = instructor
        course.save()
        module.course = course
        module.save()
        lesson.module = module
        lesson.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Update the lesson
        url = reverse('lesson-detail', args=[lesson.id])
        data = {
            'title': 'Updated Lesson Title',
            'content': 'Updated content for the lesson'
        }
        response = api_client.patch(url, data)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Lesson Title'
        assert response.data['content'] == 'Updated content for the lesson'
    
    def test_instructor_cannot_update_other_lesson(self, api_client, instructor, course, module, lesson):
        """Test that an instructor cannot update another instructor's lesson"""
        # Create another instructor who owns the course/module/lesson
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
        lesson.module = module
        lesson.save()
        
        # Authenticate as different instructor
        api_client.force_authenticate(user=instructor)
        
        # Attempt to update the lesson
        url = reverse('lesson-detail', args=[lesson.id])
        data = {
            'title': 'Should Not Update',
            'content': 'This update should fail'
        }
        response = api_client.patch(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify lesson was not updated
        lesson.refresh_from_db()
        assert lesson.title != 'Should Not Update'
    
    def test_student_cannot_update_lesson(self, api_client, student, lesson):
        """Test that a student cannot update a lesson"""
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to update the lesson
        url = reverse('lesson-detail', args=[lesson.id])
        data = {
            'title': 'Should Not Update',
            'content': 'This update should fail'
        }
        response = api_client.patch(url, data)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify lesson was not updated
        lesson.refresh_from_db()
        assert lesson.title != 'Should Not Update'
    
    def test_instructor_can_delete_own_lesson(self, api_client, instructor, course, module, lesson):
        """Test that an instructor can delete their own lesson"""
        # Set the course instructor
        course.instructor = instructor
        course.save()
        module.course = course
        module.save()
        lesson.module = module
        lesson.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Delete the lesson
        url = reverse('lesson-detail', args=[lesson.id])
        response = api_client.delete(url)
        
        # Verify response
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify lesson was deleted
        assert not Lesson.objects.filter(id=lesson.id).exists()
    
    def test_instructor_cannot_delete_other_lesson(self, api_client, instructor, course, module, lesson):
        """Test that an instructor cannot delete another instructor's lesson"""
        # Create another instructor who owns the course/module/lesson
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
        lesson.module = module
        lesson.save()
        
        # Authenticate as different instructor
        api_client.force_authenticate(user=instructor)
        
        # Attempt to delete the lesson
        url = reverse('lesson-detail', args=[lesson.id])
        response = api_client.delete(url)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify lesson was not deleted
        assert Lesson.objects.filter(id=lesson.id).exists()
    
    def test_student_cannot_delete_lesson(self, api_client, student, lesson):
        """Test that a student cannot delete a lesson"""
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to delete the lesson
        url = reverse('lesson-detail', args=[lesson.id])
        response = api_client.delete(url)
        
        # Verify response indicates permission denied
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        # Verify lesson was not deleted
        assert Lesson.objects.filter(id=lesson.id).exists()
    
    
    def test_student_can_mark_lesson_complete(self, api_client, student, course, module, lesson):
        """Test that a student can mark a lesson as complete"""
        # Make sure course is published
        course.is_published = True
        course.save()
        module.course = course
        module.save()
        lesson.module = module
        lesson.save()
        
        # Create enrollment
        enrollment = course.enrollments.create(student=student)
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Mark lesson as complete
        url = reverse('lesson-complete', args=[lesson.id])
        response = api_client.put(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        
        # Verify lesson progress was created
        assert LessonProgress.objects.filter(
            enrollment=enrollment,
            lesson=lesson,
        ).exists()
    
    
    def test_student_cannot_mark_lesson_complete_without_enrollment(self, api_client, student, course, module, lesson):
        """Test that a student cannot mark a lesson as complete without being enrolled"""
        # Make sure course is published
        course.is_published = True
        course.save()
        module.course = course
        module.save()
        lesson.module = module
        lesson.save()
        
        # Authenticate as student (with no enrollment)
        api_client.force_authenticate(user=student)
        
        # Attempt to mark lesson as complete
        url = reverse('lesson-complete', args=[lesson.id])
        response = api_client.put(url)
        
        # Verify response indicates error
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
        
        # Verify no lesson progress was created
        assert not LessonProgress.objects.filter(
            lesson=lesson
        ).exists()
    
    def test_instructor_cannot_mark_lesson_complete(self, api_client, instructor, course, module, lesson):
        """Test that an instructor cannot mark a lesson as complete (only students can)"""
        # Set up the course and instructor
        course.instructor = instructor
        course.is_published = True
        course.save()
        module.course = course
        module.save()
        lesson.module = module
        lesson.save()
        
        # Authenticate as instructor
        api_client.force_authenticate(user=instructor)
        
        # Attempt to mark lesson as complete
        url = reverse('lesson-complete', args=[lesson.id])
        response = api_client.put(url)
        
        # Verify response indicates error
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN]
        
        # Verify no lesson progress was created
        assert not LessonProgress.objects.filter(
            lesson=lesson
        ).exists() 
