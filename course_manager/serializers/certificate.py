from rest_framework import serializers

from course_manager.models.certificate import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Certificate
        fields = '__all__'
        read_only_fields = ('enrollment', 'issued_at') 
