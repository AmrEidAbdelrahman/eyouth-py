from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from account_manager.models.user import User
from course_manager.models.lesson import Lesson
from course_manager.models.module import Module
from course_manager.serializers.lesson import LessonSerializer
from course_manager.views.permissions import IsInstructorOrReadOnly, IsStudent
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from course_manager.models.enrollment import LessonProgress, Enrollment
from django.db import transaction

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]

    def get_permissions(self):
        if self.action == 'complete':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'complete' and self.request.user.role == User.Role.STUDENT:
            student_courses = self.request.user.courses_enrolled.values_list('course', flat=True)
            return super().get_queryset().filter(module__course__in=student_courses)
        if self.action == 'list' and self.request.user.role == User.Role.STUDENT:
            student_courses = self.request.user.courses_enrolled.values_list('course', flat=True)
            return super().get_queryset().filter(module__course__in=student_courses)
        return super().get_queryset()

    @transaction.atomic
    @action(detail=True, methods=['put'], url_path='complete', permission_classes=[IsStudent])
    def complete(self, request, pk=None):
        try:
            lesson = self.get_object()
            user = request.user
            if LessonProgress.objects.filter(lesson=lesson, enrollment__student=user).exists():
                return Response({'message': 'You have already completed this lesson'}, status=status.HTTP_400_BAD_REQUEST)
            print(user)
            enrollment = Enrollment.objects.get(course=lesson.module.course, student=user)
            LessonProgress.objects.create(lesson=lesson, enrollment=enrollment)
            return Response({'message': 'Lesson marked as complete'}, status=status.HTTP_200_OK)
        except Enrollment.DoesNotExist:
            return Response({'message': 'You are not enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
