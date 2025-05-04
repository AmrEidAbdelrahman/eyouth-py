from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'INSTRUCTOR'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user 
    
class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'INSTRUCTOR'
    
    
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'STUDENT'
    
    def has_object_permission(self, request, view, obj):
        return True
    
