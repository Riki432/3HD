AddWindow.py and SearchWindow.py files are merely for understanding purposes they have no use in the actual program. 
Cache.py handles the temporary files, reading and writing from them. 
TextExtractor.py makes use of pytesseract library to get text from an image. 
main.py contains all the necessary functions for the program to work. 
GUI.py has all the graphical code and makes use of other files.

If you want to execute the program, run GUI.py

The program has a dependency of Tesseract OCR which has to installed and the path for it has to be set manually.
One limitation of the program that I have noticied is that in *some* cases when the images are not in proper orientation, text extraction from the image doesn't work properly.
