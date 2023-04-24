import re
from django.core.exceptions import ValidationError


def hex_validator(hex_string):
    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string)
    if not match:
        raise ValidationError(message='Не корректный HEX цвет')
