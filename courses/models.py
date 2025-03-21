from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons')

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
