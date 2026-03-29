from rest_framework.viewsets import ReadOnlyModeViewset
from rest_framework.permissions import AllowAny
from .serializers import CourseListSerializer, CourseDetailSerializer
from ..models import Course

class CourseViewSet(ReadOnlyModeViewset):#DRF джанги сам делает urls капец умный
    quieryset=Course.objects.all()
    permissionclasses=[AllowAny]

    def get_queryset(self):
        if self.action=='list':
            return self.quieryset.filter(published=True)
        return self.quieryset

    def get_serializer_class(self):
        if self.action=='list':
            return CourseListSerializer
        return CourseDetailSerializer
