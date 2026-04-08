from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as f
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from ..models import *
from ..filters import *

class CourseViewSet(ReadOnlyModelViewSet): #DRF джанги сам делает urls капец умный
    quieryset=Course.objects.all()
    permissionclasses=[AllowAny]

    filter_backends = [DjangoFilterBackend, f.SearchFilter,]
    filterset_class = CoursesFilter
    search_fields = ['title']

    def get_queryset(self):
        if self.action=='list':
            return self.quieryset.filter(published=True)
        return self.quieryset

    def get_serializer_class(self):
        if self.action=='list':
            return CourseListSerializer
        return CourseDetailSerializer


class LessonsViewSet(ReadOnlyModelViewSet):
    queryset=Lesson.objects.all()

    def get_serializer_class(self):
        if self.action=='list':
            return LessonSerializer
        return LessonSerializer


class UserProfileViewSet(ReadOnlyModelViewSet):
    queryset=UserProfile.objects.all()

    def get_serializer_class(self):
        if self.action=='list':
            return UserProfileSerializer
        return UserProfileSerializer
    

class EnrollmentViewSet(ModelViewSet):
    queryset=Enrollment.objects.all()
    # serializer_class = EnrollmentCreateSerializer
    permission_classes=[IsAuthenticated]

    def get_serializer_class(self):
        if self.action=='create':
            return EnrollmentCreateSerializer
        return EnrollmentListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     user_id=self.request.user.id 
    #     instance=self.get_object()
    #     serializer=self.get_serializer(instance, data=request.data)
