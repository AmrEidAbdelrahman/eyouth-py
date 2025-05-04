from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from account_manager.models.user import User
from course_manager.models.course import Course
from course_manager.models.enrollment import Enrollment
from course_manager.serializers.course import CourseSerializer
from course_manager.serializers.enrollment import EnrollmentSerializer
from course_manager.views.permissions import IsInstructor, IsInstructorOrReadOnly, IsStudent
from course_manager.serializers.module import ModuleSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructorOrReadOnly]

    def get_permissions(self):
        if self.action in 'enroll':
            return [permissions.IsAuthenticated(), IsStudent()]
        return super().get_permissions()

    def check_object_permissions(self, request, obj):
        if request.user.role == User.Role.INSTRUCTOR and obj.instructor != request.user:
            self.permission_denied(request)
        
        if request.user.role == User.Role.STUDENT and self.action == 'enroll':
            return True
        
        return super().check_object_permissions(request, obj)

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def get_queryset(self):
        if self.action == 'list' and self.request.user.role == User.Role.INSTRUCTOR:
            return super().get_queryset().filter(instructor=self.request.user)
        elif self.action == 'enroll':
            return super().get_queryset().filter(is_published=True)
        return super().get_queryset()


    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        course = self.get_object()
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response(
                {'detail': 'Already enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        enrollment = Enrollment.objects.create(student=request.user, course=course)
        return Response(
            EnrollmentSerializer(enrollment).data,
            status=status.HTTP_201_CREATED
        ) 

    @action(detail=True, methods=['post'], url_path='add-module')
    def add_module(self, request, pk=None):
        course = self.get_object()
        data = request.data
        data['course'] = course.id
        serializer = ModuleSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        module = serializer.save(course=course)
        return Response(
            ModuleSerializer(module).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'], url_path='enrollments')
    def enrollments(self, request, pk=None):
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course)
        return Response(
            EnrollmentSerializer(enrollments, many=True).data
        )

