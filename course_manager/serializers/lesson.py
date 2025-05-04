from rest_framework import serializers
from course_manager.models.enrollment import LessonProgress
from course_manager.models.lesson import Lesson

class LessonSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()

    def get_completed(self, obj):
        if 'request' not in self.context:
            return False
        if self.context['request'].user.is_authenticated:
            return LessonProgress.objects.filter(lesson=obj, enrollment__student=self.context['request'].user).exists()
        return False
        

    class Meta:
        model = Lesson
        fields = '__all__' 
