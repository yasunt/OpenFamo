from django.core.exceptions import ValidationError


def validate_content(content):
    '''Raise a ValidationError if the content contains only URL string.'''

    if False:
        message = '''Can't post a content with only URL string.'''
        raise ValidationError(message)
