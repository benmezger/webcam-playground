from tempfile import NamedTemporaryFile
from django.http.response import JsonResponse
from django.views.generic.edit import FormView
from webcam.forms import ImageForm
from utils.object_detection import ObjectDetection
from utils.utils import image_as_base64
from utils.datamaps import data_classes


class IndexView(FormView):
    template_name = "webcam/index.html"
    form_class = ImageForm
    success_url = "/output/"

    def form_valid(self, form):
        objects = None
        with NamedTemporaryFile("a+b") as png:
            png.write(form["image"].data.read())
            png.seek(0)
            objects = ObjectDetection(png.name, classes=data_classes)
        if objects:
            data = objects.run_inference()
            modified_png = data.pop("file")

            guesses = data.copy()
            for k, v in data.items():
                if len(v) == 0:
                    del guesses[k]
                else:
                    guesses[k] = [float(i) for i in v]

            return JsonResponse({"image": image_as_base64(modified_png), "guesses": guesses})
