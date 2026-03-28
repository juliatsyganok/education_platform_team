from rest_framework import serializers
from django.contrib.auth import User 
from ..models import Course, Lesson, UserProfile

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        models=Lesson
        fields=['id','name','description','video_url','content','order']

class CourseListSerializer(serializers.ModelSerializer):
    lesson_count=serializers.IntegerField(source='lesson.count',read_only=True)
    author=serializers.ChatField(source='author.user.username',read_only=True)
    class Meta:
        model=Course
        fields=['id','title','description','price','created_at','lesson_count','author']
    
class CourseDetailSerializer(serializers.ModelSerializer):
    lessons=LessonSerializer(many=True,read_only=True)
    author=serializers.CharField(source='author.user.username', read_only=True)
    class Meta:
        model=Course
        fields=['id', 'title', 'description', 'price', 'created_at', 'published', 'author', 'lessons']