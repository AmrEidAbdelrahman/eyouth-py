from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import TokenSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=User.Role.choices)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def custom_signup(self, request, user):
        user.role = self.validated_data.get('role', User.Role.STUDENT)
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'bio', 'profile_picture')
        read_only_fields = ('email', 'role') 

class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')
