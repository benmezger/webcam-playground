import os
import base64

def image_as_base64(image_file, format='png'):
    encoded_string = ''
    encoded_string = base64.b64encode(image_file.file.read())
    return 'data:image/%s;base64,%s' % (format, encoded_string)
