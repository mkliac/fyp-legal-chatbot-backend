import os
import docx2txt
from pdf2image import convert_from_path
import pytesseract
import re
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"PyTesseract-additional-packages\tesseract\tesseract.exe"
poppler_path = r"PyTesseract-additional-packages\Release-22.04.0-0\poppler-22.04.0\Library\bin"

class Extractor():

    def getExtension(self, filename):
        tokens = os.path.splitext(filename)
        return tokens[-1]
    
    def extract(self, filename):
        extension = self.getExtension(filename)
        text = ""

        if(extension == ".txt"):
            text = self.txt2str(filename)
        elif(extension == ".docx"):
            text = self.docx2str(filename)
        elif(extension == ".pdf"):
            text = self.pdf2str(filename)
        elif(extension == ".png"):
            text = self.png2str(filename)
        else:
            return False

        text = self.filter(text)

        return text
    
    def filter(self, text):
        # Remove non-ascii codes
        text = ''.join([i if ord(i) < 128 else ' ' for i in text])
        # Remove unwanted symbols
        unwanted = r"|`<>=_()[]~{}"
        for char in unwanted:
            text = text.replace(char, "")
        # Remove duplicated spaces
        text = " ".join(text.split())
        
        return text
    
    def txt2str(self, filename):
        text = ""
        with open(filename) as f:
            text = f.read()
        
        return text

    def docx2str(self, filename):
        text = docx2txt.process(filename)

        return text

    def pdf2str(self, filename):
        text = ""
        
        images = convert_from_path(filename, poppler_path=poppler_path)
        for image in images:
            text += pytesseract.image_to_string(image) + "\n"
        
        return text
    
    def png2str(self, filename):
        image = Image.open(filename)
        text = pytesseract.image_to_string(image)
        return text

# Testing 
if __name__ == "__main__":
    # testing files
    path = r"Extraction-test-files\testFile"
    extractor = Extractor()
    
    content = extractor.extract(path + ".png")
    print(content)
