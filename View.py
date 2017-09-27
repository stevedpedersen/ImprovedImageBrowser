# File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.

import Model, os, sys
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSoundEffect

class View(QWidget):

	def __init__(self, windowWidth, files):
		super().__init__()
		self.title = 'Project 2 - Improved Image Browser'
		self.model = Model.Model(self)
		self.model.initModel(windowWidth, files)
		self.labels = self.model.generateLabels(self, 6)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.model.getWindowWidth(), self.model.getWindowHeight())
		self.setStyleSheet('background-color: white')
		self.draw() 
		self.show()

	# Attach images to labels in thumbnail or fullscreen mode
	def draw(self):	
		self.clearBrowser()
		mode = self.model.getMode()
		# TODO: Setup handler for left and select being too far apart
		leftmost = self.model.getLeftmostIndex()
		selected = self.model.getSelectedIndex()
		
		# Thumbnail Mode
		if mode == 0:	
			y = self.model.getWindowHeight() - (self.model.getThumbHeight() * 2) 
			for i in range(5):
				x = int(((self.model.getWindowWidth() - self.model.getThumbWidth()*5)/2) + i*self.model.getThumbWidth())
				# Center the highlighted thumbnail when returning from full screen mode
				thumb = (leftmost + i) % len(self.model.getFiles())				
				color = 'green'
				if thumb == selected:
					color = 'red'	
				
				self.attachPixmap(thumb, i, x, y, self.model.getThumbWidth(), self.model.getThumbHeight(), self.model.getThumbBorder(), color)
		
		# Full Screen Mode		
		elif mode == 1:
			x = (self.model.getWindowWidth() - self.model.getFullWidth()) / 2
			y = (self.model.getWindowHeight() - self.model.getFullHeight()) / 2
			self.attachPixmap(selected, 5, x, y, self.model.getFullWidth(), self.model.getFullHeight(), self.model.getFullBorder(), 'red')

	# Assigns an image to one of the labels
	def attachPixmap(self, pindex, lindex, x, y, w, h, b, color):
		#print(pindex, lindex, x, y, w, h, b, color)
		mode = 0
		if lindex == 5:
			mode = 1

		self.labels[lindex].setPixIndex(pindex)
		self.labels[lindex].setPixmap(self.model.getPixmap(mode, pindex))
		self.labels[lindex].setAlignment(Qt.AlignCenter)
		self.labels[lindex].setGeometry(QRect(x, y, w, h))
		self.labels[lindex].setStyleSheet('border: ' + str(b) + 'px solid '+ color)
		self.labels[lindex].clicked.connect(self.mouseSel)
		self.labels[lindex].show()

	# Type is 0=short, 1=medium, 2=long
	def playSound(self, soundType = 0):
		soundFile = 'long.wav'
		if soundType == 0:
			soundFile = 'short.wav'
		elif soundType == 1:
			soundFile = 'medium.wav'

		self.sound = QSoundEffect()
		self.sound.setSource(QUrl.fromLocalFile(os.path.join('audio', soundFile)))
		self.sound.setLoopCount(1)
		self.sound.play()
		# self.sound.stop()		
		
	# Full screen mode on clicked label while in thumbnail mode
	def mouseSel(self, label, testStr):
		if self.model.getMode() == 0:
			self.model.setMode(1)
			self.model.setSelectedIndex(label.getPixIndex())

		self.draw()		
	
	# TODO: Bugfix
	# Handles key events and responds according to current browser state
	def keyPressEvent(self, event):
		up = 16777235
		down = 16777237
		left = 16777234
		right = 16777236
		scrollL = 44
		scrollR = 46
		thumb = 0
		full = 1

		# Enter Full Screen Mode
		if self.model.getMode() == thumb and event.key() == up:
			self.model.setMode(1)
			self.playSound(1)
		# Exit Full Screen Mode			
		elif self.model.getMode() == full and event.key() == down:
			self.model.setMode(0)
			self.model.setLeftmostIndex(self.model.getSelectedIndex() - 2)
			self.playSound(1)
		# Left - Full Screen
		elif self.model.getMode() == full and event.key() == left:
			self.model.setSelectedIndex(self.model.getSelectedIndex() - 1)
			self.playSound(0)
		# Right - Full Screen		
		elif self.model.getMode() == full and event.key() == right:
			self.model.setSelectedIndex(self.model.getSelectedIndex() + 1)
			self.playSound(0)
		# Left - Thumbnail
		elif self.model.getMode() == thumb and event.key() == left:
			selected = self.model.getSelectedIndex()
			leftmost = self.model.getLeftmostIndex()
			newIndex = (selected - 1) % len(self.model.getFiles())
			#print('Left move. New Index: '+str(newIndex))
			if newIndex < leftmost or newIndex > selected:
				self.model.setLeftmostIndex(leftmost - 5)
			# elif ():
			self.model.setSelectedIndex(newIndex)
			self.playSound(0)
		# Right - Thumbnail		
		elif self.model.getMode() == thumb and event.key() == right:
			selected = self.model.getSelectedIndex()
			leftmost = self.model.getLeftmostIndex()
			newIndex = (selected + 1) % len(self.model.getFiles())
			# TODO: bugfix - moving right when left > newIndex
			if newIndex > ((leftmost + 4) % len(self.model.getFiles())):
				self.model.setLeftmostIndex(leftmost + 5)
			self.model.setSelectedIndex(newIndex)
			self.playSound(0)
		# Next set Left - Thumbnail		
		elif self.model.getMode() == thumb and event.key() == scrollL:
			selected = self.model.getSelectedIndex()
			newIndex = (selected - 5) % len(self.model.getFiles())
			self.model.setSelectedIndex(newIndex)
			self.model.setLeftmostIndex(newIndex)
			self.playSound(2)
		# Next set Right - Thumbnail		
		elif self.model.getMode() == thumb and event.key() == scrollR:
			selected = self.model.getSelectedIndex()
			newIndex = (selected + 5) % len(self.model.getFiles())
			self.model.setSelectedIndex(newIndex)
			self.model.setLeftmostIndex(newIndex)
			self.playSound(2)

		print('Leftmost: '+str(self.model.getLeftmostIndex())+'\tSelected: '+str(self.model.getSelectedIndex()))

		self.draw()

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			# self.labels[i].setStyleSheet('border: none')
			self.labels[i].hide()


