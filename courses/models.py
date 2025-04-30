from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title


@login_required
@permission_required('courses.can_edit_course', raise_exception=True)
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.owner != request.user and not request.user.groups.filter(name='Moderators').exists():
        return HttpResponseForbidden("У вас нет прав для редактирования этого курса.")
    # Логика редактирования
    return render(request, 'edit_course.html', {'course': course})
