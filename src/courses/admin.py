from django.contrib import admin
from .models import Course, Lesson, Enrollment, UserProfile

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['title', 'author', 'price', 'published', 'created_at']
    list_filter = ['published', 'author']
    search_fields = ['title']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=['course', 'name', 'order']
    list_filter = ['course']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=['username', 'email', 'date_joined']
    search_fields=['username', 'email']

    def username(self, obj):
        return obj.user.username
    
    
    def email(self, obj):
        return obj.user.email
    

    def date_joined(self, obj):
        return obj.user.date_joined


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'date_enrolled', 'status']
