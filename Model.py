# File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.


import os, sys
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
		

class Model(QLabel):

	# when QLabel is clicked, emit a signal with an object param
	clicked = pyqtSignal(object, str)

	def __init__(self, parent):
		super().__init__(parent)
		self.selectedIndex = 0
		self.leftmostIndex = 0
		self.pixIndex = 0
		self.mode = 0
		self.images = []

	def initModel(self, windowWidth, files):
		self.setDimensions(windowWidth)
		self.setFiles(files)
		self.generatePixmaps(files)
		

	def generateLabels(self, window, quantity):
		labels = []
		for _ in range(quantity):
			labels.append(Model(window))
		return labels	

	def generatePixmaps(self, files):
		thumbs = []
		fulls = []
		for f in files:		
			thumb = self.resizeAndFrame('data/' + f, self.thumbWidth, self.thumbHeight, self.thumbBorder)
			full = self.resizeAndFrame('data/' + f, self.fullWidth, self.fullHeight, self.fullBorder)
			thumbs.append(thumb)
			fulls.append(full)

		self.images.append(thumbs)
		self.images.append(fulls)	

	def getPixmap(self, mode, index):
		# print(self.images[mode][index])
		return self.images[mode][index]

	# Scale image to width or height based on image orientation	& label dimensions
	def resizeAndFrame(self, filename, w, h, b):		
		pixmap = QPixmap(filename)		
		if pixmap.width() > pixmap.height():
			pixmap = pixmap.scaledToWidth(w - 2*b)
			if pixmap.height() > (h - 2*b):
				pixmap = pixmap.scaledToHeight(h - 2*b)
		else:
			pixmap = pixmap.scaledToHeight(h - 2*b)

		return pixmap

	def setFiles(self, files):
		self.files = files

	# Scales everything that is displayed according to window width
	def setDimensions(self, windowWidth):
		self.setWindowWidth	( int(windowWidth) )
		self.setWindowHeight( int(3 * self.windowWidth / 4) )
		self.setThumbWidth	( int(self.windowWidth / 6) )
		self.setThumbHeight	( int(3 * self.thumbWidth / 4) )
		self.setThumbBorder	( int(self.windowWidth / (self.thumbWidth * 0.75)) )
		self.setFullWidth	( int(self.windowWidth * 0.9) )
		self.setFullHeight	( int(3 * self.fullWidth / 4) )
		self.setFullBorder	( int(self.windowWidth / (self.thumbWidth * 0.25)) )

	def mousePressEvent(self, event):
		# on click sends the object name to mouseSel()
		self.clicked.emit(self, 'PIX INDEX: ' + str(self.getPixIndex))

	def setPixIndex(self, i):
		self.pixIndex = i
	def getPixIndex(self):
		return self.pixIndex

	def getWindowWidth(self):
		return self.windowWidth
	def setWindowWidth(self, w):
		self.windowWidth = w
	def getWindowHeight(self):
		return self.windowHeight
	def setWindowHeight(self, h):
		self.windowHeight = h
	
	def getThumbWidth(self):
		return self.thumbWidth
	def setThumbWidth(self, w):
		self.thumbWidth = w
	def getThumbHeight(self):
		return self.thumbHeight
	def setThumbHeight(self, h):
		self.thumbHeight = h
	def getThumbBorder(self):
		return self.thumbBorder
	def setThumbBorder(self, b):
		self.thumbBorder = b
	
	def getFullWidth(self):
		return self.fullWidth
	def setFullWidth(self, w):
		self.fullWidth = w
	def getFullHeight(self):
		return self.fullHeight
	def setFullHeight(self, h):
		self.fullHeight = h
	def getFullBorder(self):
		return self.fullBorder
	def setFullBorder(self, b):
		self.fullBorder = b

	def getSelectedIndex(self):
		return self.selectedIndex
	def setSelectedIndex(self, index):
		self.selectedIndex = index % len(self.getFiles())		
	def getLeftmostIndex(self):
		return self.leftmostIndex
	def setLeftmostIndex(self, index):
		self.leftmostIndex = index % len(self.getFiles())
	def getMode(self):
		return self.mode
	def setMode(self, mode):
		self.mode = mode	
	def getImages(self):
		return self.images
	def getFiles(self):
		return self.files



