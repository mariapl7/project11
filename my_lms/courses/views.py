from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CourseListView(APIView):
    def get(self, request):
        # Здесь вы можете вернуть список курсов
        courses = [
            {"id": 1, "title": "Курс 1", "description": "Описание курса 1"},
            {"id": 2, "title": "Курс 2", "description": "Описание курса 2"},
        ]
        return Response(courses, status=status.HTTP_200_OK)
