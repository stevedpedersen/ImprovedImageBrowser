# File: project1.py
# By: Steve Pedersen
# Date: September 12, 2017
# Usage: python3 project1.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.

import Model
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from itertools import cycle
from PyQt5.QtCore import *

class View(QWidget):

	def __init__(self, windowWidth, files):
		super().__init__()
		self.title = 'Project 2 - Improved Image Browser'
		self.model = Model.Model(self)
		self.model.initModel(windowWidth, files)
		labels = self.model.generateLabels(6)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.model.getWindowWidth(), self.model.getWindowHeight())
		self.setStyleSheet('background-color: #B5B2C2;')

		self.draw(0, 0, 0) 

		self.show()

	# TODO: THIS IS WHERE I'VE LEFT OFF!!!!!!!!!!!!!*********************************************
	# Attach images to labels in thumbnail or fullscreen mode
	def draw(self, mode, selected, centered = -1):
		if self.mode != mode:
			self.clearBrowser()
		self.mode = mode
		
		self.h = (selected - 1) % len(self.files)
		self.i = (selected) 	% len(self.files)
		self.j = (selected + 1) % len(self.files)

		# Thumbnail Mode
		if mode == 0:	
			y = self.height - (self.thumbH * 2) 
			for i in range(5):
				x = ((self.width - self.thumbW*5)/2) + i*self.thumbW
				# Center the highlighted thumbnail when returning from full screen mode
				if centered > 0:
					thumb = (centered + i) % len(self.files)
				else:
					thumb = (selected + i) % len(self.files)				
				color = '#A0C1D1'
				if thumb == selected:
					color = '#5A7D7C'	

				self.attachPixmap(thumb, i, x, y, self.thumbW, self.thumbH, self.thumbB, color)
		
		# Full Screen Mode		
		elif mode == 1:
			x = (self.width - self.fullW) / 2
			y = (self.height - self.fullH) / 2
			self.attachPixmap(selected, 5, x, y, self.fullW, self.fullH, self.fullB, '#5A7D7C')

	# Assigns an image to one of the labels
	def attachPixmap(self, pindex, lindex, x, y, w, h, b, color):
		mode = 0
		if lindex == 5:
			mode = 1
		self.labels[lindex].pixIndex = pindex
		self.labels[lindex].labIndex = lindex
		self.labels[lindex].setVisible(True)
		self.labels[lindex].setPixmap(self.images[mode][pindex])
		self.labels[lindex].setAlignment(Qt.AlignCenter)
		self.labels[lindex].setGeometry(QRect(x, y, w, h))
		self.labels[lindex].setStyleSheet('border: ' + str(b) + 'px solid '+ color+';')
		self.labels[lindex].clicked.connect(self.mouseSel)	

	def mouseSel(self, label):
		if self.mode == 0:
			self.draw(1, label.pixIndex)
	
	# Handles key events and responds according to current browser state
	def keyPressEvent(self, event):
		up = 16777235
		down = 16777237
		left = 16777234
		right = 16777236
		scrollL = 44
		scrollR = 46

		# Enter Full Screen Mode
		if self.mode == 0 	and event.key() == up:
			self.draw(1, self.i)
		# Exit Full Screen Mode			
		elif self.mode == 1 and event.key() == down:
			self.draw(0, self.i, (self.i - 2) % len(self.files))
		# Left - Full Screen
		elif self.mode == 1 and event.key() == left:
			self.draw(1, self.h)
		# Right - Full Screen		
		elif self.mode == 1 and event.key() == right:
			self.draw(1, self.j)
		# Left - Thumbnail
		elif self.mode == 0 and event.key() == left:
			self.draw(0, self.h)
		# Right - Thumbnail		
		elif self.mode == 0 and event.key() == right:
			self.draw(0, self.j)
		# Next set Left - Thumbnail		
		elif self.mode == 0 and event.key() == scrollL:
			nextIndex = (self.i - 5) % len(self.files)
			self.draw(0, nextIndex, nextIndex)
		# Next set Right - Thumbnail		
		elif self.mode == 0 and event.key() == scrollR:
			nextIndex = (self.i + 5) % len(self.files)
			self.draw(0, nextIndex, nextIndex)

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			self.labels[i].setStyleSheet('border: none')
			self.labels[i].setVisible(False)		