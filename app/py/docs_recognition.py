from PIL import Image
import pytesseract
import cv2
import os
import re

class Recognizer:
    def __init__(self):
        pass

    def get_doc_text(self, filepath, median_blur=3):
        image = cv2.imread(filepath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, median_blur)

        config = ("-l rus --oem 1 --psm 3")
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        text = pytesseract.image_to_string(Image.open(filename), config=config)
        os.remove(filename)

        return text

    def parse_text_as_SNILS(self, text):

        text = re.sub(r'\n', ' ', text)
        m = re.match(r'.*([0-9]{3}-[0-9]{3}-[0-9]{3}[ -][0-9]{2}).*', text)
        if m is not None:
            return {'id':m.group(1)}
        return None

    def recognize_SNILS_file(self, filepath):
        try:
            text = self.get_doc_text(filepath=filepath)
            data = self.parse_text_as_SNILS(text)
            return data
        except Exception as e:
            print('cant recognize ', filepath, ': ', e)

    def parse_text_as_OMS(self, text):

        text = re.sub(r'\n', ' ', text)
        m = re.match(r'.*([0-9]{16}).*', text)
        if m is not None:
            return {'id':m.group(1)}
        return None

    def recognize_OMS_file(self, filepath):
        try:
            text = self.get_doc_text(filepath=filepath)
            data = self.parse_text_as_OMS(text)
            return data
        except Exception as e:
            print('cant recognize ', filepath, ': ', e)

if __name__ == '__main__':
    filename = input('type img filename: ')
    recog = Recognizer()
    text = recog.get_doc_text(filepath=filename)
    print(text)

