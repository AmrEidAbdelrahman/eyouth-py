from rest_framework import serializers
from account_manager.serializers.user import UserSerializer
from course_manager.models.enrollment import Enrollment, LessonProgress

class EnrollmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('student', 'completed', 'completed_at')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        if 'student' in res:
            res['student'] = UserSerializer(instance.student).data
        return res
