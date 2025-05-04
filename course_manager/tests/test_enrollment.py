import pytest
from django.urls import reverse
from rest_framework import status
from course_manager.models import Enrollment, LessonProgress

@pytest.mark.django_db
class TestEnrollmentAPI:
    
    def test_student_can_enroll_in_course(self, api_client, student, course):
        """Test that a student can enroll in a published course"""
        # Make sure course is published
        course.is_published = True
        course.save()
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Enroll in course
        url = reverse('course-enroll', args=[course.id])
        response = api_client.post(url)
        
        # Verify response
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify enrollment was created
        assert Enrollment.objects.filter(student=student, course=course).exists()
        
    def test_student_cannot_enroll_in_unpublished_course(self, api_client, student, course):
        """Test that a student cannot enroll in an unpublished course"""
        # Make sure course is not published
        course.is_published = False
        course.save()
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to enroll in course
        url = reverse('course-enroll', args=[course.id])
        response = api_client.post(url)
        
        # Verify response
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Verify enrollment was not created
        assert not Enrollment.objects.filter(student=student, course=course).exists()
        
    def test_student_cannot_enroll_twice(self, api_client, student, course):
        """Test that a student cannot enroll in the same course twice"""
        # Make sure course is published
        course.is_published = True
        course.save()
        
        # Create existing enrollment
        Enrollment.objects.create(student=student, course=course)
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Attempt to enroll in course again
        url = reverse('course-enroll', args=[course.id])
        response = api_client.post(url)
        
        # Verify response indicates conflict
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Verify only one enrollment exists
        assert Enrollment.objects.filter(student=student, course=course).count() == 1
    
    def test_track_lesson_progress(self, api_client, student, course, module, lesson):
        """Test that a student's lesson progress is tracked correctly"""
        # Create enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Mark lesson as complete
        url = reverse('lesson-complete', args=[lesson.id])
        response = api_client.put(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        
        # Verify lesson progress was recorded
        assert LessonProgress.objects.filter(
            enrollment=enrollment,
            lesson=lesson,
        ).exists()
        
    def test_course_completion(self, api_client, student, course, module):
        """Test that a course is marked as completed when all lessons are completed"""
        # Create enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        
        # Create two lessons in the module
        lesson1 = module.lessons.create(
            title='Lesson 1',
            content_type='TEXT',
            content='Content 1',
            order=1
        )
        
        lesson2 = module.lessons.create(
            title='Lesson 2',
            content_type='TEXT',
            content='Content 2',
            order=2
        )
        
        # Authenticate as student
        api_client.force_authenticate(user=student)
        
        # Mark first lesson as complete
        url = reverse('lesson-complete', args=[lesson1.id])
        api_client.put(url)
        
        # Verify enrollment is not completed yet
        enrollment.refresh_from_db()
        assert enrollment.completed == False
        
        
        # Mark second lesson as complete
        url = reverse('lesson-complete', args=[lesson2.id])
        response = api_client.put(url)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        
        # Verify enrollment is now marked as completed
        enrollment.refresh_from_db()
        assert enrollment.completed == True
        assert enrollment.completed_at is not None 
