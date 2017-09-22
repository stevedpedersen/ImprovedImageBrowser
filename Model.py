# File: project1.py
# By: Steve Pedersen
# Date: September 12, 2017
# Usage: python3 project1.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.


import os, sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from itertools import cycle
from PyQt5.QtCore import *

class ClickableLabel(QLabel):
	# when QLabel is clicked, emit a signal with an object param
	clicked = pyqtSignal(object)

	def __init__(self, parent):
		super().__init__(parent)
		self.pixIndex = 0

	def mousePressEvent(self, event):
		# on click sends the object name to mouseSel()
		self.clicked.emit(self)

class Model(QLabel):

	def __init__(self, parent):
		super().__init__(parent)
		self.selectedIndex = 0
		self.leftmostIndex = 0
		self.mode = 0

	def initModel(self, windowWidth, files):
		self.setDimensions(windowWidth)
		self.setFiles(files)
		self.generateLabels(files)
		

	def generateLabels(self, quantity):
		labels = []
		for _ in range(quantity):
			labels.append(ClickableLabel(self))
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
		self.windowWidth = int(windowWidth)
		self.windowHeight = int(3 * self.windowWidth / 4)
		self.thumbWidth = int(self.windowWidth / 6)
		self.thumbHeight = int(3 * self.thumbWidth / 4)
		self.thumbBorder = int(self.windowWidth / (self.thumbWidth * 0.75))
		self.fullWidth 	= int(self.windowWidth * 0.9)
		self.fullHeight	= int(3 * self.fullWidth / 4)
		self.fullBorder	= int(self.windowWidth / (self.thumbWidth * 0.25))

	def getWindowWidth(self):
		return self.windowWidth
	def getWindowHeight(self):
		return self.windowHeight
	def getThumbWidth(self):
		return self.thumbWidth
	def getThumbHeight(self):
		return self.thumbHeight
	def getThumbBorder(self):
		return self.thumbBorder
	def getFullWidth(self):
		return self.fullWidth
	def getFullHeight(self):
		return self.thumbHeight
	def getFullBorder(self):
		return self.thumbBorder

	def getSelectedIndex(self):
		return self.selectedIndex
	def getLeftmostIndex(self):
		return self.leftmostIndex
	def getMode(self):
		return self.mode
	def getImages(self):
		return self.images
	def getFiles(self):
		return self.files



