from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import *


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    
    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Название урока должно быть не менее 3 символов")
        return value
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Урок не может быть пустым")
        return value
    
    def validate_order(self, value):
        course = self.initial_data.get('course')
        if course:
            instance_id = self.instance.id if self.instance else None
            exists = Lesson.objects.filter(course_id=course, order=value)
            if instance_id:
                exists = exists.exclude(id=instance_id)
            if exists.exists():
                raise serializers.ValidationError(f"Урок с номером {value} уже существует в этом курсе")
        return value


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    author = serializers.CharField(source='author.user.username', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'lessons_count', 'created_at', 'author']

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.user.username', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'created_at', 'published', 'author', 'lessons']
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Название должно быть не менее 5 символов")
        return value
    
    def validate_description(self, value):
        if len(value.strip()) < 50:
            raise serializers.ValidationError(f"Описание должно быть не менее 50 символов")
        return value
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio', 'image']
    
    def validate_bio(self, value):
        if len(value) > 500:
            raise serializers.ValidationError("Описание не должно превышать 500 символов")
        return value
    
    def validate_image(self, value):
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Размер изображения не должен превышать 2 МБ")
        return value


class EnrollmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        exclude = ['user']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Enrollment.objects.create(**validated_data)
    
    def validate_course(self, value):
        if not value.published:
            raise serializers.ValidationError("Нельзя записаться на неопубликованный курс")
        return value
    
    def validate(self, data):
        user = self.context['request'].user
        course = data.get('course')
        
        if Enrollment.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError({
                'course': 'Вы уже записаны на этот курс'
            })
        
        return data