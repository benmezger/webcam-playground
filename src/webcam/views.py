from tempfile import NamedTemporaryFile
from django.http.response import JsonResponse
from django.views.generic.edit import FormView
from webcam.forms import ImageForm
from utils.object_detection import ObjectDetection
from utils.utils import image_as_base64


class IndexView(FormView):
    template_name = "webcam/index.html"
    form_class = ImageForm
    success_url = "/output/"

    def form_valid(self, form):
        objects = None
        with NamedTemporaryFile("a+b") as png:
            png.write(form["image"].data.read())
            png.seek(0)
            objects = ObjectDetection(png.name)
        if objects:
            modified_png = objects.run_inference()
            return JsonResponse({"image": image_as_base64(modified_png)})
