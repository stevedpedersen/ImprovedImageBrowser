 # File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py 
# System: OS X
# Dependencies: Python3, PyQt5
# Description: Creates an image browser that displays images as 
# 	thumbnails and fullscreen. Navigation with keys and mouse.

import Model, os, sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QAction, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSoundEffect

class View(QWidget):

	buttonStyle = 'background-color: #d3d3d3; padding: 5px; border: 1px solid #000; border-radius: 3px;'

	def __init__(self, windowWidth, files):
		super().__init__()
		self.title = 'Project 2.5 - Improved Image Browser'
		self.model = Model.Model(self)
		self.model.initModel(windowWidth, files)
		self.labels = self.model.generateLabels(self, 6)
		self.initUI()
		self.show()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.model.getWindowWidth(), self.model.getWindowHeight())
		self.setStyleSheet('background-color: #FFFFFF;')	
		self.showSearchComponents()
		self.initTags()
		self.draw() 
		self.show()
		self.setFocus()

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
			self.hideTagComponents()
			self.hideTags()
			self.showSearchComponents()

		# Full Screen Mode		
		elif mode == 1:
			x = (self.model.getWindowWidth() - self.model.getFullWidth()) / 2
			y = (self.model.getWindowHeight() - self.model.getFullHeight()) / 2
			self.attachPixmap(selected, 5, x, y, self.model.getFullWidth(), self.model.getFullHeight(), self.model.getFullBorder(), 'red')
			self.showTagComponents()
			self.showTags()
			# self.hideSearchComponents()

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

	def showSearchComponents(self):
		padding = self.model.getFullBorder()
		windowWidth = self.model.getWindowWidth()
		windowHeight = self.model.getWindowHeight()	

		self.searchComponents = []
		self.searchTextBox = QLineEdit(self)	
		self.searchTextBox.resize(windowWidth/2.5, padding*1.5)
		self.searchTextBox.move(padding, windowHeight - padding*2)
		self.searchTextBox.setStyleSheet('border: 1px solid #868e96;')	
		self.searchTextBox.setPlaceholderText('Search Flickr...')

		# connect button to functions search()
		self.searchButton = QPushButton('Search', self)
		self.searchButton.clicked.connect(self.search)
		self.searchButton.setStyleSheet(View.buttonStyle)
		self.searchButton.move(windowWidth/2, windowHeight - padding*1.7)

		self.searchComponents.append(self.searchTextBox)
		self.searchComponents.append(self.searchButton)
		for t in self.searchComponents:
			t.show()

	def hideSearchComponents(self):
		for t in self.searchComponents:
			t.hide()
			t.setVisible(False)

	def search(self):
		print(self.searchTextBox.text())

	# Pre-load all tags for each image into a dictionary
	def initTags(self):
		self.tagTextBox = QLineEdit(self)	
		self.tagComponents, self.tagDict = [], {}
		self.tagComponents.append(self.tagTextBox)
		self.tags = [] # QPushButton 'tags' List

		# create a dict { imgFileName1: [tag1, tag2], ... }
		imgFileNames = self.model.getFiles()
		self.tagDict = {name: [] for name in imgFileNames}

		tagFileNames = os.listdir('tags')
		for f in tagFileNames:
			file = open('tags/' + f, 'r')
			fNameNoExt = f[0:f.find('.txt')]
			for imgName in imgFileNames:
				if imgName == fNameNoExt:
					tags = file.readlines()
					tags = [x.strip() for x in tags] 
					for tag in tags:
						self.tagDict[imgName].append(tag)
			file.close()								

	# Displays all tags for currently selected image
	def showTags(self):
		self.hideTags()
		self.tags = []
		padding = self.model.getFullBorder()
		currTagKey = self.model.getFiles()[self.model.getSelectedIndex()]

		for i in range(len(self.tagDict[currTagKey])):
			self.tags.append(QPushButton(self.tagDict[currTagKey][i], self))
			self.tags[i].setStyleSheet(View.buttonStyle)
			self.tags[i].move(padding/4, padding + padding*i*1.4)
			self.tags[i].show()

	def hideTags(self):
		for t in self.tags:
			t.hide()
			t.setVisible(False)
		self.tags = []


	# Add textbox, buttons, and tags
	def showTagComponents(self):
		padding = self.model.getFullBorder()
		windowWidth = self.model.getWindowWidth()
		windowHeight = self.model.getWindowHeight()

		self.tagTextBox.resize(windowWidth/3, padding*1.5)
		self.tagTextBox.move(padding, windowHeight - padding*2)
		self.tagTextBox.setStyleSheet('border: 1px solid #868e96;')
		self.tagTextBox.setPlaceholderText('Enter tag text...')

		# connect button to functions add/saveTags
		self.addButton = QPushButton('Add Tag', self)
		self.saveButton = QPushButton('Save All Tags', self)
		self.addButton.clicked.connect(self.addTag)
		self.saveButton.clicked.connect(self.saveTags)
		self.addButton.setStyleSheet(View.buttonStyle)
		self.saveButton.setStyleSheet(View.buttonStyle)

		self.addButton.move(windowWidth/2, windowHeight - padding*1.7)
		self.saveButton.move(windowWidth/1.5, windowHeight - padding*1.7)

		self.tagComponents.append(self.addButton)
		self.tagComponents.append(self.saveButton)
		for t in self.tagComponents:
			t.show()

	def hideTagComponents(self):
		for t in self.tagComponents:
			t.hide()

	# Writes tags to files with .txt appended to the image name
	# For example, if image filename is Test0.png then tag filename is Test0.png.txt
	def saveTags(self):
		for filename, taglist in self.tagDict.items():
			if len(taglist) > 0:
				file = open('tags/' + filename + '.txt', 'w')
				for i, tag in enumerate(taglist):
					tag = tag.strip('\n')
					if i != (len(taglist) - 1):
						file.write(tag + '\n')
					else:
						file.write(tag)
				file.close()

	# Creates a tag for current image from textbox
	def addTag(self):
		textBoxStr = self.tagTextBox.text()	
		if textBoxStr != "":
			# add to list of tags for current image
			currTagKey = self.model.getFiles()[self.model.getSelectedIndex()]
			self.tagDict[currTagKey].append(textBoxStr)

		self.showTags()
		self.tagTextBox.setText('')
		self.setFocus()

	# Type is 0=short, 1=medium, 2=long
	def playSound(self, soundType = 0):
		if soundType == 0:
			soundFile = 'short.wav'
		elif soundType == 1:
			soundFile = 'medium.wav'
		elif soundType == 2:
			soundFile = 'long.wav'

		self.sound = QSoundEffect()
		self.sound.setSource(QUrl.fromLocalFile(os.path.join('audio', soundFile)))
		self.sound.setLoopCount(1)
		self.sound.play()	
		
	# Full screen mode on clicked label while in thumbnail mode
	def mouseSel(self, label):
		if self.model.getMode() == 0:
			self.model.setMode(1)
			self.model.setSelectedIndex(label.getPixIndex())
		self.setFocus()
		self.draw()		
	
	# Handles key events and responds according to current browser state
	def keyPressEvent(self, event):
		up, down, left, right = 16777235, 16777237, 16777234, 16777236
		scrollL, scrollR = 44, 46
		thumb, full = 0, 1
		short, medium, big = 0, 1, 2
		tab, esc, enter = 16777217, 16777216, 16777220
		currentMode = self.model.getMode()
		# print(event.key())

		# Enter Full Screen Mode
		if currentMode == thumb and event.key() == up:
			self.model.setMode(full)
			self.playSound(medium)
		# Exit Full Screen Mode			
		elif currentMode == full and event.key() == down:
			self.model.setMode(thumb)
			self.model.setLeftmostIndex(self.model.getSelectedIndex() - 2)
			self.playSound(medium)
		# Left - Full Screen
		elif currentMode == full and event.key() == left:
			self.model.setSelectedIndex(self.model.getSelectedIndex() - 1)
			self.playSound(short)
		# Right - Full Screen		
		elif currentMode == full and event.key() == right:
			self.model.setSelectedIndex(self.model.getSelectedIndex() + 1)
			self.playSound(short)
		# Left - Thumbnail
		elif currentMode == thumb and event.key() == left:
			selected = self.model.getSelectedIndex()
			leftmost = self.model.getLeftmostIndex()
			newIndex = (selected - 1) % len(self.model.getFiles())
			if selected == leftmost:
				self.model.setLeftmostIndex(leftmost - 5)
			self.model.setSelectedIndex(newIndex)
			self.playSound(short)
		# Right - Thumbnail		
		elif currentMode == thumb and event.key() == right:
			selected = self.model.getSelectedIndex()
			leftmost = self.model.getLeftmostIndex()
			newIndex = (selected + 1) % len(self.model.getFiles())
			if selected == ((leftmost + 4) % len(self.model.getFiles())):
				self.model.setLeftmostIndex(leftmost + 5)
			self.model.setSelectedIndex(newIndex)
			self.playSound(short)
		# Next set Left - Thumbnail		
		elif currentMode == thumb and event.key() == scrollL:
			selected = self.model.getSelectedIndex()
			newIndex = (selected - 5) % len(self.model.getFiles())
			self.model.setSelectedIndex(newIndex)
			self.model.setLeftmostIndex(newIndex)
			self.playSound(big)
		# Next set Right - Thumbnail		
		elif currentMode == thumb and event.key() == scrollR:
			selected = self.model.getSelectedIndex()
			newIndex = (selected + 5) % len(self.model.getFiles())
			self.model.setSelectedIndex(newIndex)
			self.model.setLeftmostIndex(newIndex)
			self.playSound(big)
		elif currentMode == full and event.key() == enter:
			self.addTag()

		# print('Leftmost: '+str(self.model.getLeftmostIndex())+'\tSelected: '+str(self.model.getSelectedIndex()))
		self.draw()

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			self.labels[i].hide()
		self.hideTags()
		self.hideSearchComponents()
		# self.hideTagComponents()

