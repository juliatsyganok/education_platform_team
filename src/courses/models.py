from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(
        blank=True,
        validators=[MaxLengthValidator(500, message="Описание не должно превышать 500 символов")],
        help_text="Краткая информация о пользователе"
    )
    image = models.ImageField(
        upload_to="profile_images/", 
        blank=True,
        help_text="Фото профиля. Максимальный размер 2MB"
    )

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Название курса (от 5 до 200 символов)"
    )
    description = models.TextField(
        help_text="Подробное описание курса (минимум 50 символов)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[
            MinValueValidator(0, message="Цена не может быть отрицательной"),
            MaxValueValidator(1000000, message="Цена не может превышать 1 000 000")
        ],
        help_text="Цена в рублях от 0 до 1 000 000"
    )
    published = models.BooleanField(
        default=False,
        help_text="Опубликовать курс"
    )
    author = models.ForeignKey(
        UserProfile, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="courses"
    )

    class Meta:
        unique_together = [['title', 'author']]

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.title.strip() == "":
            raise ValidationError({'title': 'Название не может состоять только из пробелов'})
        
        if len(self.title.strip()) < 5:
            raise ValidationError({'title': 'Название должно быть не менее 5 символов'})
        
        if len(self.description.strip()) < 50:
            raise ValidationError({
                'description': f'Описание должно быть не менее 50 символов'
            })


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="lessons"
    )
    name = models.CharField(
        max_length=200,
        help_text="Название урока"
    )
    description = models.TextField(
        blank=True,
        help_text="Краткое описание урока"
    )
    video_url = models.URLField(
        blank=True,
        help_text="Ссылка на видео"
    )
    content = models.TextField(
        help_text="Основной контент урока"
    )
    order = models.PositiveIntegerField(
        validators=[MinValueValidator(1, message="Номер должен быть не менее 1")],
        help_text="Номмер урока в курсе"
    )

    class Meta:
        ordering = ["order"]
        unique_together = [['course', 'order']]

    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.content.strip():
            raise ValidationError({'content': 'Урок не может быть пустым'})
        
        if len(self.name.strip()) < 3:
            raise ValidationError({'name': 'Название урока должно быть не менее 3 символов'})


class Enrollment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        help_text="Студент"
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        help_text="Курс, на который записан студент"
    )
    date_enrolled = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ("active", "активна"), 
        ("cancelled", "отменена"),
        ("completed", "завершена")
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="active",
        help_text="Статус записи на курс"
    )

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курсы"

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
    def clean(self):
        if not self.course.published:
            raise ValidationError({
                'course': 'Нельзя записаться на неопубликованный курс'
            })
        
        if hasattr(self.user, 'userprofile') and self.user.userprofile == self.course.author:
            raise ValidationError({
                'user': 'Автор курса не может записаться'
            })
        
class LessonProgress(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='lesson_progress',
        verbose_name="Студент"
    )
    lesson = models.ForeignKey(
        'Lesson', 
        on_delete=models.CASCADE, 
        related_name='progress_records',
        verbose_name="Урок"
    )
    is_completed = models.BooleanField(
        default=False, 
        verbose_name="Пройден"
    )
    completed_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата прохождения"
    )

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name = "Прогресс урока"
        verbose_name_plural = "Прогресс уроков"

    def __str__(self):
        status = "Пройден" if self.is_completed else "В процессе"
        return f"{self.user.username} - {self.lesson.name}: {status}"