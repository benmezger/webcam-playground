from tempfile import NamedTemporaryFile
import tensorflow
import tensornets
import cv2
import numpy


class ObjectDetection:
    def __init__(self, image, classes={}):
        self.image_capture = cv2.imread(image)

        self.inputs = tensorflow.placeholder(tensorflow.float32, [None, 416, 416, 3])
        self.model = tensornets.YOLOv3COCO(
            self.inputs, tensornets.Darknet19, reuse=tensorflow.AUTO_REUSE
        )

        self.classes = classes
        if not bool(classes):
            self.classes = {"0": "person", "15": "cat", "67": "cell phone"}

    def run_inference(self):

        with tensorflow.Session() as sess:
            np_load_old = numpy.load
            numpy.load = lambda *a, **k: np_load_old(*a, **k)
            sess.run(self.model.pretrained())
            numpy.load = np_load_old

            out_file = NamedTemporaryFile("a+b", suffix=".jpg")
            img = cv2.resize(self.image_capture, (820, 820))
            # cv2.namedWindow("image", cv2.WINDOW_NORMAL)
            # cv2.resizeWindow("image", 700, 700)

            imge = numpy.array(img).reshape(-1, 820, 820, 3)

            preds = sess.run(
                self.model.preds, {self.inputs: self.model.preprocess(imge)}
            )

            boxes = numpy.array(self.model.get_boxes(preds, imge.shape[1:3]))

            for j in self.classes.keys():

                if j in self.classes:
                    lab = self.classes[str(j)]

                j = int(j)

                if len(boxes) > 0:
                    for i in range(len(boxes[j])):
                        box = boxes[j][i]
                        if boxes[j][i][4] >= 0.40:

                            cv2.rectangle(
                                img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 1
                            )

                            cv2.putText(
                                img,
                                lab,
                                (box[0], box[1]),
                                cv2.FONT_HERSHEY_TRIPLEX,
                                0.9,
                                (0, 0, 255),
                                lineType=cv2.LINE_AA,
                            )

            cv2.imwrite(f"{out_file.name}", img)
            # cv2.imshow("image", img)
            # if cv2.waitKey(0) & 0xFF == ord("q"):
            #     break
        return out_file


if __name__ == "__main__":
    webcam = ObjectDetection()
    webcam.run_inference()
