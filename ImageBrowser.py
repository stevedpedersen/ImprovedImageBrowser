# File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py <Window Width (int)> <Safe Mode (0/1)>
# Usage Example 800x600 window in Safe Mode: python3 ImageBrowser.py 800 1
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as thumbnails and fullscreen.
#	Navigation with keys and mouse. Add tags to images and save them. Search the Flickr
#	database for images to add to the image browser. Safe Mode gives confirmation on exit/delete
#	as well as limits number of search results.


import os, sys, View
from PyQt5.QtWidgets import QApplication, QLabel

# Create an image browser from the images in the 'data' folder
if __name__ == '__main__':
	app = QApplication(sys.argv)
	windowWidth = sys.argv[1] if len(sys.argv) == 2 else 800
	imageFiles = os.listdir('data')
	safeMode = False
	if len(sys.argv) == 3 and sys.argv[2] == 1:
		safeMode = True
	view = View.View(windowWidth, imageFiles, safeMode)
	sys.exit(app.exec_())    
	