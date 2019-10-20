from webcam.forms import VideoForm
from django.views.generic.edit import FormView


class IndexView(FormView):
    template_name = "webcam/index.html"
    form_class = VideoForm
    success_url = "/output/"

    def form_valid(self, form):
        pass
