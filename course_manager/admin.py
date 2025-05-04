from django.contrib import admin
from django.contrib import admin

from course_manager.models.course import Course
from course_manager.models.module import Module
from course_manager.models.lesson import Lesson
from course_manager.models.enrollment import Enrollment, LessonProgress
from course_manager.models.certificate import Certificate

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'created_at', 'instructor')
    search_fields = ('title', 'description', 'instructor__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'content_type', 'order', 'created_at')
    list_filter = ('content_type', 'created_at', 'module__course')
    search_fields = ('title', 'content', 'module__title')
    ordering = ('module', 'order')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed', 'completed_at')
    list_filter = ('completed', 'enrolled_at', 'completed_at')
    search_fields = ('student__email', 'course__title')
    date_hierarchy = 'enrolled_at'
    readonly_fields = ('enrolled_at',)

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed_at')
    list_filter = ('completed_at',)
    search_fields = ('enrollment__student__email', 'lesson__title')
    readonly_fields = ('completed_at',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('enrollment__student__email', 'enrollment__course__title')
    readonly_fields = ('issued_at',)
    date_hierarchy = 'issued_at' 
