import threading
import cv2


class VideoCamera(object):
    def __init__(self, threads=False):
        self.video = cv2.VideoCapture(0)

        if threads:
            self.__grabbed, self.__frame = self.video.read()
            threading.Thread(target=self.__update, args=()).start()

    def __del__(self):
        self.video.release()

    def __iter__(self):
        if self.video.isOpened():
            _, frame = self.video.read()
            yield frame

    def __update(self):
        while self.video.isOpened():
            (self.__grabbed, self.__frame) = self.video.read()
