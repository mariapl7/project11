from django.test import TestCase
from rest_framework.exceptions import ValidationError
from .validators import youtube_link_validator


def test_valid_youtube_link():
    valid_link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert youtube_link_validator(valid_link) == valid_link


def test_invalid_link():
    invalid_link = "https://www.example.com"
    try:
        youtube_link_validator(invalid_link)
    except ValidationError as e:
        assert str(e) == "Ссылка должна быть на youtube.com"
