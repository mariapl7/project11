import re
from rest_framework.exceptions import ValidationError


def youtube_link_validator(value):
    """Проверка, что ссылка ведет только на youtube.com."""
    youtube_regex = r'^https://(www\.)?youtube\.com/.*$'
    if not re.match(youtube_regex, value):
        raise ValidationError("Ссылка должна быть на youtube.com")
    return value
