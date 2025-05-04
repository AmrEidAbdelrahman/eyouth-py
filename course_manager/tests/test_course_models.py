import pytest
from django.contrib.auth import get_user_model
from course_manager.models import Course, Enrollment, Module, Lesson, LessonProgress

User = get_user_model()

@pytest.mark.django_db
class TestCourseModel:
    
    def test_get_progress_with_no_lessons(self, course, student):
        """Test progress calculation when a course has no lessons"""
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
         )
        
        # Calculate progress
        progress = course.get_progress(student)
        
        # Assert progress is 0 when no lessons exist
        assert progress == 0
    
    def test_get_progress_with_no_completed_lessons(self, course, module, lesson, student):
        """Test progress calculation when no lessons are completed"""
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
         )
        
        # Calculate progress
        progress = course.get_progress(student)
        
        # Assert progress is 0% when no lessons are completed
        assert progress == 0
    
    def test_get_progress_with_some_completed_lessons(self, course, module, student):
        """Test progress calculation with some completed lessons"""
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
         )
        
        # Create two lessons in the module
        lesson1 = Lesson.objects.create(
            module=module,
            title='Lesson 1',
            content_type='TEXT',
            content='Content 1',
            order=1
        )
        
        lesson2 = Lesson.objects.create(
            module=module,
            title='Lesson 2',
            content_type='TEXT',
            content='Content 2',
            order=2
        )
        
        # Complete one lesson
        LessonProgress.objects.create(
            enrollment=enrollment,
            lesson=lesson1,
        )
        
        # Calculate progress
        progress = course.get_progress(student)
        
        # Assert progress is 50% (1 out of 2 lessons)
        assert progress == 50.0
    
    def test_get_progress_with_all_completed_lessons(self, course, module, student):
        """Test progress calculation with all lessons completed"""
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
         )
        
        # Create two lessons in the module
        lesson1 = Lesson.objects.create(
            module=module,
            title='Lesson 1',
            content_type='TEXT',
            content='Content 1',
            order=1
        )
        
        lesson2 = Lesson.objects.create(
            module=module,
            title='Lesson 2',
            content_type='TEXT',
            content='Content 2',
            order=2
        )
        
        # Complete both lessons
        LessonProgress.objects.create(
            enrollment=enrollment,
            lesson=lesson1,
        )
        
        LessonProgress.objects.create(
            enrollment=enrollment,
            lesson=lesson2,
        )
        
        # Calculate progress
        progress = course.get_progress(student)
        
        # Assert progress is 100%
        assert progress == 100.0 
