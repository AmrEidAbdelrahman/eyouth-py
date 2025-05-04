from rest_framework import serializers
from course_manager.models.module import Module
from course_manager.serializers.lesson import LessonSerializer

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = '__all__'
        extra_kwargs = {
            'course': {
                'required': False
            }
        }
