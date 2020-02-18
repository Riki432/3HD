from PIL import Image
import pytesseract
import cv2

def getText(filename):
    '''
    Takes a file name and returns the text in that file.
    '''
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text
