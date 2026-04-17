from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router=DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('lessons', LessonsViewSet, basename='lessons')
router.register('users', UserProfileViewSet, basename='userprofile')
router.register('enrollments', EnrollmentViewSet, basename='enrollments')

urlpatterns=[
    path('', include(router.urls))
]
