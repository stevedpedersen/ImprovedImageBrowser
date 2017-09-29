# File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as thumbnails and fullscreen.
#	Navigation with keys and mouse. Add tags to images and save them. Search the Flickr
#	database for images to add to the image browser.


import os, sys, View
from PyQt5.QtWidgets import QApplication, QLabel

# Create an image browser from the images in the 'data' folder
if __name__ == '__main__':
	app = QApplication(sys.argv)
	windowWidth = sys.argv[1] if len(sys.argv) == 2 else 800
	files = os.listdir('data')
	view = View.View(windowWidth, files)
	sys.exit(app.exec_())    
	