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
		self.labels = self.model.generateLabels(6)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.model.getWindowWidth(), self.model.getWindowHeight())
		self.setStyleSheet('background-color: #B5B2C2;')
		self.draw() 
		self.show()

	# Attach images to labels in thumbnail or fullscreen mode
	def draw(self):	# REMOVE THESE PARAMETERS....
		# self.clearBrowser()
		# self.model.setMode(mode)
		# self.model.setSelectedIndex(selected)
		mode = self.model.getMode()
		selected = self.model.getSelectedIndex()
		centered = -1
		
		# Thumbnail Mode
		if mode == 0:	
			y = self.model.getWindowHeight() - (self.model.getThumbHeight() * 2) 
			for i in range(5):
				x = int(((self.model.getWindowWidth() - self.model.getThumbWidth()*5)/2) + i*self.model.getThumbWidth())
				# Center the highlighted thumbnail when returning from full screen mode
				if centered > 0:
					thumb = (centered + i) % len(self.model.getFiles())
				else:
					thumb = (selected + i) % len(self.model.getFiles())				
				color = '#A0C1D1'
				if thumb == selected:
					color = '#5A7D7C'	
				
				self.attachPixmap(thumb, i, x, y, self.model.getThumbWidth(), self.model.getThumbHeight(), self.model.getThumbBorder(), color)
		
		# Full Screen Mode		
		elif mode == 1:
			x = (self.model.getWindowWidth() - self.model.getFullWidth()) / 2
			y = (self.model.getWindowHeight() - self.model.getFullHeight()) / 2
			self.attachPixmap(selected, 5, x, y, self.model.getFullWidth(), self.model.getFullHeight(), self.model.getFullBorder(), '#5A7D7C')

	# Assigns an image to one of the labels
	def attachPixmap(self, pindex, lindex, x, y, w, h, b, color):
		print(pindex, lindex, x, y, w, h, b, color)
		mode = 0
		if lindex == 5:
			mode = 1
		self.labels[lindex].setPixIndex(pindex)
		# self.labels[lindex].labIndex = lindex
		# self.labels[lindex].setVisible(True)
		
		self.labels[lindex].setPixmap(self.model.getPixmap(mode, pindex))
		# print(self.labels[lindex].pixmap())
		self.labels[lindex].setAlignment(Qt.AlignCenter)
		self.labels[lindex].setGeometry(QRect(x, y, w, h))
		self.labels[lindex].setStyleSheet('border: ' + str(b) + 'px solid '+ color+';')
		self.labels[lindex].clicked.connect(self.mouseSel)
		self.labels[lindex].setText('SOME TEXT FOOL')
		# print(self.labels[lindex].parent)

	def mouseSel(self, label):
		if self.model.getMode() == 0:
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
		if self.model.getMode() == 0 and event.key() == up:
			self.draw(1, self.i)
		# Exit Full Screen Mode			
		elif self.model.getMode() == 1 and event.key() == down:
			self.draw(0, self.i, (self.i - 2) % len(self.model.getFiles()))
		# Left - Full Screen
		elif self.model.getMode() == 1 and event.key() == left:
			self.draw(1, self.h)
		# Right - Full Screen		
		elif self.model.getMode() == 1 and event.key() == right:
			self.draw(1, self.j)
		# Left - Thumbnail
		elif self.model.getMode() == 0 and event.key() == left:
			self.draw(0, self.h)
		# Right - Thumbnail		
		elif self.model.getMode() == 0 and event.key() == right:
			self.draw(0, self.j)
		# Next set Left - Thumbnail		
		elif self.model.getMode() == 0 and event.key() == scrollL:
			nextIndex = (self.i - 5) % len(self.model.getFiles())
			self.draw(0, nextIndex, nextIndex)
		# Next set Right - Thumbnail		
		elif self.model.getMode() == 0 and event.key() == scrollR:
			nextIndex = (self.i + 5) % len(self.model.getFiles())
			self.draw(0, nextIndex, nextIndex)

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			self.labels[i].setStyleSheet('border: none')
			self.labels[i].setVisible(False)		