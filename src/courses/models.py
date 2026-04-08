from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="profile_images/", blank=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, related_name="cources"
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    content = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (("active", "активна"), ("cancelled", "отменена"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
