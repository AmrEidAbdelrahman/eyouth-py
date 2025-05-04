from django.urls import path, include
from rest_framework import routers

from course_manager.views.certificate import CertificateViewSet
from course_manager.views.course import CourseViewSet
from course_manager.views.lesson import LessonViewSet
from course_manager.views.module import ModuleViewSet


router = routers.DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
router.register('certificates', CertificateViewSet, basename='certificate')
router.register('modules', ModuleViewSet, basename='module')
router.register('lessons', LessonViewSet, basename='lesson')


urlpatterns = [
    path('', include(router.urls)),
] 
