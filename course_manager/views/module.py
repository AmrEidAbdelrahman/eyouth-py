from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from account_manager.models.user import User
from course_manager.models.module import Module
from course_manager.models.course import Course
from course_manager.serializers.module import ModuleSerializer
from rest_framework.decorators import action
from course_manager.serializers.lesson import LessonSerializer
from rest_framework.response import Response
from course_manager.views.permissions import IsInstructor, IsInstructorOrReadOnly

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]
    

    def get_queryset(self):
        if self.action == 'list':
            return Module.objects.filter(course__instructor=self.request.user)
        return Module.objects.all()
    
    # already implemented as Course action
    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        if course.instructor != self.request.user:
            self.permission_denied(self.request)
        serializer.save(course=course)

    @action(detail=True, methods=['post'], url_path='add-lesson', url_name='add-lesson')
    def add_lesson(self, request, pk):
        module = self.get_object()
        data = request.data
        data['module'] = pk
        serializer = LessonSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        lesson = serializer.save(module=module)
        return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)
