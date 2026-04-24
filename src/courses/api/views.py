from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as f

from ..services import *
from ..services.course_progress import complete_lesson_service, get_course_progress
from .serializers import *
from ..models import *
from ..filters import *


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, f.SearchFilter]
    filterset_class = CoursesFilter
    search_fields = ['title']

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(published=True)
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

    @action(methods=['get'], detail=True, url_path='enroll', url_name='make_enroll')
    def make_enroll(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = EnrollmentCreateSerializer(
            data={"course": course.pk},
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        result = EnrollmentService.create_enrollment(user=request.user, course=course)

        return Response({
            "success": True,
            "course_id": course.pk,
            "message": "Вы успешно записаны на курс"
        })


class LessonsViewSet(ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return LessonSerializer

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        try:
            complete_lesson_service(user=request.user, lesson_id=pk)
            return Response({"status": "success", "message": "Урок пройден"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """
        GET /api/lessons/{id}/progress/
        Возвращает прогресс по курсу, к которому относится этот урок
        """
        lesson = self.get_object()
        try:
            data = get_course_progress(user=request.user, course=lesson.course)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_serializer_class(self):
        return UserProfileSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        return EnrollmentListSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data['course']
        payment_success = PaymentService.make_a_payment(float(course.price))
        if not payment_success:
            raise ValidationError({"payment": "Оплата не прошла"})
        serializer.save(user=user)