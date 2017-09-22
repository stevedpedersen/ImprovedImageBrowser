# File: project1.py
# By: Steve Pedersen
# Date: September 12, 2017
# Usage: python3 project1.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.


import os, sys, Model, View
from PyQt5.QtWidgets import QApplication, QLabel

# Create an image browser from the images in the 'data' folder
if __name__ == '__main__':
	app = QApplication(sys.argv)
	# imageBrowser = ImageBrowser(os.listdir('data'))
	windowWidth = sys.argv[1] if len(sys.argv) == 2 else 800
	files = os.listdir('data')
	view = View.View(windowWidth, files)
	sys.exit(app.exec_())    
	
