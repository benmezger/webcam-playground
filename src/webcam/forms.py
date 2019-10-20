from django import forms
from django.core.validators import FileExtensionValidator

import filetype


class VideoForm(forms.Form):
    video = forms.FileField(validators=(FileExtensionValidator,))

    def clean_video(self):
        data = self.cleaned_data['video']
        kind = filetype.guess(data.read())
        data.seek(0)

        if kind is None:
            return False
        return kind.mime == 'video/webm'
