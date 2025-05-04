from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from account_manager.serializers.user import UserSerializer
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions() 
