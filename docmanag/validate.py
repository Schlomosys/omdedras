from django.core.exceptions import ValidationError
def maximum_size(width=None, height=None):
    def validator(image):
        if not image.is_image():
            raise ValidationError('File should be image.')

        errors, image_info = [], image.info()['image_info']
        if width is not None and image_info['width'] > width:
            errors.append('Width should be < {} px.'.format(width))
        if height is not None and image_info['height'] > height:
            errors.append('Height should be < {} px.'.format(height))
        raise ValidationError(errors)
    return validator


def validator_image(image):
        if not image.is_image():
            raise ValidationError('File should be image.')

        file_size = image.file.size
        limit_kb = 150
        if file_size > limit_kb * 1024:
            raise ValidationError("Max size of file is %s KB" % limit_kb)

  