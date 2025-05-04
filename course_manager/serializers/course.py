from rest_framework import serializers
from course_manager.models.course import Course
from course_manager.models.enrollment import Enrollment
from course_manager.serializers.module import ModuleSerializer

class CourseSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField(source='get_progress')
    modules = ModuleSerializer(many=True, read_only=True)

    def get_progress(self, obj):
        if not 'request' in self.context:
            return None
        user = self.context['request'].user
        if Enrollment.objects.filter(course=obj, student=user).exists():
            return obj.get_progress(user)
        return None
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('instructor',)

    