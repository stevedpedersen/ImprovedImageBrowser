# File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py <Window Width (int)> <Safe Mode (0/1)>
# Usage Example 800x600 window in Safe Mode: python3 ImageBrowser.py 800 1
# System: OS X
# Dependencies: Python3, PyQt5, requests, Flickr API key saved in a file with a name 
#	prepended with 'apikey' (e.g. apikey-flickr)
# Description: Creates an image browser that displays images as thumbnails and fullscreen.
#	Navigation with keys and mouse. Add tags to images and save them. Search the Flickr
#	database for images to add to the image browser. Safe Mode gives confirmation on exit/delete
#	as well as limits number of search results.


import os, sys, View
from PyQt5.QtWidgets import QApplication

# Create an image browser from the images in the 'data' folder
if __name__ == '__main__':
	app = QApplication(sys.argv)

	# Open with user defined window width. Defaults to a 800x600 window.
	windowWidth = sys.argv[1] if len(sys.argv) > 1 else 800

	# Open with image files stored in 'data' directory
	imageFiles = os.listdir('data')

	# Open in Safe Mode?
	safeMode = False
	if len(sys.argv) == 3 and sys.argv[2] == '1':
		safeMode = True

	# Open with Search feature? Requires API Key in a file.
	apiKeyExists = False
	files = os.listdir('./')
	for f in files:
		if f.find('apikey') == 0:
			print('API key found: ', f)
			apiKeyExists = True
	if not apiKeyExists:
		print(
			'No API Key found. \nImageBrowser requires API Key to be saved in a file in root dir \n'
			'with a name prepended with "apikey" (e.g. apikey-flickr).\n'
			'Opening Image Browser without Search feature...'
		)

	# Open ImageBrowser with specified parameters
	view = View.View(windowWidth, imageFiles, safeMode, apiKeyExists)

	sys.exit(app.exec_())    
	