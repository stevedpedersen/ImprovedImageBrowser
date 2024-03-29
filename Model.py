# File: Model.py
# By: Steve Pedersen
# Date: October 1, 2017
# Usage: python3 ImageBrowser.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Model class. Can be used to generate QLabels and to
#		keep track of data state.


import os, sys
from urllib.request import urlopen
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import *
from PyQt5 import QtNetwork, QtCore
		

class Model(QLabel):

	# when QLabel is clicked, emit a signal with an object param
	clicked = pyqtSignal(object)

	def __init__(self, parent):
		super().__init__(parent)
		self.selectedIndex = 0
		self.leftmostIndex = 0
		self.pixIndex = 0
		self.mode = 0
		self.images = []
		self.imageCount = 0
		self.thumbQty = 5
		self.view = parent
		self.searchQty = 0
		self.searchCount = 0
		self.appendIndex = 0
		self.newFiles = {}

	def initModel(self, windowWidth, files, thumbQty):
		self.setThumbQty(thumbQty)
		self.setDimensions(windowWidth)
		self.setFiles(files)
		self.generatePixmaps(files)
		
	# Creates a list of Models (QLabels) of <quantity> length, connected to window (QWidget)
	def generateLabels(self, window, quantity):
		labels = []
		for _ in range(quantity):
			labels.append(Model(window))
		return labels	

	# Creates a 2D list of thumbnail & fullscreen pixmaps from a file list
	def generatePixmaps(self, files, remoteSrc = False):
		thumbs = []
		fulls = []
		for f in files:		
			thumb = self.resizeAndFrame('data/' + f, self.thumbWidth, self.thumbHeight, self.thumbBorder)
			full = self.resizeAndFrame('data/' + f, self.fullWidth, self.fullHeight, self.fullBorder)
			thumbs.append(thumb)
			fulls.append(full)
			self.imageCount += 1

		self.images.append(thumbs)
		self.images.append(fulls)	

	# Fetch images from the web from their URL, create Pixmaps, then add to images 2D list
	def requestImages(self, urls):
		self.searchQty = len(urls)
		self.nam = QtNetwork.QNetworkAccessManager()
		self.nam.finished.connect(self.handleImageResponse)		
		fileNames = []
		for url in urls:		
			k = url.rfind("/")
			imgFileName = url[k+1:]	
			fileNames.append(imgFileName)

			req = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
			self.nam.get(req)
		
		return fileNames

	# Handler from QNetworkAccessManager request made in requestImages()
	# Uses raw data from response and creates Pixmaps to be displayed in Browser
	def handleImageResponse(self, reply):
		er = reply.error()
		if er == QtNetwork.QNetworkReply.NoError:
			if self.searchCount == 0:
				self.appendIndex = self.getImageCount()-1

			url_data = reply.readAll()
			thumb = self.resizeAndFrame(url_data, self.thumbWidth, self.thumbHeight, self.thumbBorder)
			full = self.resizeAndFrame(url_data, self.fullWidth, self.fullHeight, self.fullBorder)

			self.images[0].append(thumb)
			self.images[1].append(full)
			self.imageCount += 1
			self.searchCount +=1

			# end of full image search
			if self.searchQty == self.searchCount:
				# print('new leftmost and selected: ', self.getSelectedIndex() - self.searchQty)
				self.setLeftmostIndex(self.getImageCount() - self.searchQty)
				self.setSelectedIndex(self.getImageCount() - self.searchQty)
				self.searchQty, self.searchCount = 0, 0
				if self.view.statusText is not None:
					self.view.statusText.setText('')	
				self.view.setFocus()
						
			self.view.draw()
			self.view.initTags()
			# self.view.statusText.setText('Success!')

	# Scale image to width or height based on image orientation	& label dimensions
	def resizeAndFrame(self, file, w, h, b):	
		pixmap = QPixmap()	
		if isinstance(file, str):
			pixmap = QPixmap(file)
		else:
			pixmap.loadFromData(file)
		
		if pixmap.width() > pixmap.height():
			pixmap = pixmap.scaledToWidth(w - 2*b)
			if pixmap.height() > (h - 2*b):
				pixmap = pixmap.scaledToHeight(h - 2*b)
		else:
			pixmap = pixmap.scaledToHeight(h - 2*b)

		return pixmap

	# Scales everything that is displayed according to window width
	def setDimensions(self, windowWidth):
		self.setWindowWidth	( int(windowWidth) )
		self.setWindowHeight( int(3 * self.windowWidth / 4) )
		self.setThumbWidth	( int(self.windowWidth / (self.getThumbQty() + 1)) )
		self.setThumbHeight	( int(3 * self.thumbWidth / 4) )
		self.setThumbBorder	( int(self.windowWidth / (self.thumbWidth * 0.75)) )
		self.setFullWidth	( int(self.windowWidth * 0.7) )
		self.setFullHeight	( int(3 * self.fullWidth / 4) )
		self.setFullBorder	( int(self.windowWidth / (self.thumbWidth * 0.25)) )

	# Overriden method. Emits signal of type Model object (QLabel)
	def mousePressEvent(self, event):
		# on click sends Model object to mouseSel()
		self.clicked.emit(self)

	def getApiKey(self, service='flickr'):
		file = open('apikey-' + service, 'r')
		return file.read().strip()

	def getThumbQty(self):
		return self.thumbQty
	def setThumbQty(self, qty):
		self.thumbQty = qty;

	def getPixmap(self, mode, index):
		return self.images[mode][index]
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
		self.thumbBorder = b if b < 10 else 5
	
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
		self.fullBorder = b if b < 26 else 25

	def getSelectedIndex(self):
		return self.selectedIndex
	def setSelectedIndex(self, index):
		if self.getImageCount() > 0:
			self.selectedIndex = index % self.getImageCount()
		else:
			self.selectedIndex = 0
	def getLeftmostIndex(self):
		return self.leftmostIndex
	def setLeftmostIndex(self, index):
		if self.getImageCount() > 0:
			self.leftmostIndex = index % self.getImageCount()
		else:
			self.leftmostIndex = 0
	def getMode(self):
		return self.mode
	def setMode(self, mode):
		self.mode = mode
	def getFile(self, index):
		if index < self.getImageCount():
			return self.files[index]	
	def getFiles(self):
		return self.files
	def setFiles(self, files):
		for i, f in enumerate(files):
			if f.rfind('.') == 0:
				# print('Deleted hidden file: ', f)
				del files[i]
		self.files = files
	def addFiles(self, files, urls = None):
		for i, file in enumerate(files):
			self.files.append(file)
			if urls != None:
				self.newFiles[file] = urls[i]
	def clearNewFiles(self):
		self.newFiles = {}
	def getNewFiles(self):
		return self.newFiles

	def getImages(self):
		return self.images			
	def getImageCount(self):
		return self.imageCount
	def deleteImage(self, filename, index):
		try:
		    os.remove('data/' + filename)
		except OSError:
		    pass		
		del self.files[index]
		del self.images[0][index]
		del self.images[1][index]
		self.imageCount -= 1


###################    End Model Class    ###################