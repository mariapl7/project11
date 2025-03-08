from django.db import models
from users.models import CustomUser


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title
