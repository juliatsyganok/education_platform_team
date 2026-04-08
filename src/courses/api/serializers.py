from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        # fields=['id','name','description','video_url','content','order']
        fields = '__all__'

class CourseListSerializer(serializers.ModelSerializer):
    # lessons_count=serializers.IntegerField(source='lesson.course',read_only=True)
    lessons_count=serializers.SerializerMethodField()
    author=serializers.CharField(source='author.user.username',read_only=True)
    class Meta:
        model=Course
        fields=['id','title','description','price','lessons_count', 'created_at','author']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons=LessonSerializer(many=True,read_only=True)
    author=serializers.CharField(source='author.user.username', read_only=True)
    class Meta:
        model=Course
        fields=['id', 'title', 'description', 'price', 'created_at', 'published', 'author', 'lessons']


class UserProfileSerializer(serializers.ModelSerializer):
    username=serializers.CharField(source='user.username')
    email=serializers.EmailField(source='user.email')
    # date_joined=serializers.DateTimeField(source='user.date_joined')
    class Meta:
        model=UserProfile
        depth=1
        # fields='__all__'
        fields=['username', 'email', 'bio', 'image']


class EnrollmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        exclude=['user']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=['course']

    def create(self, validated_data):
        return Enrollment.objects.create(**validated_data)




