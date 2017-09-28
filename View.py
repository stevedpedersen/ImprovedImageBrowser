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

	def __init__(self, windowWidth, files):
		super().__init__()
		self.title = 'Project 2.5 - Improved Image Browser'
		self.model = Model.Model(self)
		self.model.initModel(windowWidth, files)
		self.labels = self.model.generateLabels(self, 6)
		self.initTags()
		self.initUI()
		self.show()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.model.getWindowWidth(), self.model.getWindowHeight())
		self.setStyleSheet('background-color: #FFFFF8;')

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
			self.hideTagComponents()

		# Full Screen Mode		
		elif mode == 1:
			x = (self.model.getWindowWidth() - self.model.getFullWidth()) / 2
			y = (self.model.getWindowHeight() - self.model.getFullHeight()) / 2
			self.attachPixmap(selected, 5, x, y, self.model.getFullWidth(), self.model.getFullHeight(), self.model.getFullBorder(), 'red')
			self.showTagComponents()

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

	def initTags(self):
		self.textbox = QLineEdit(self)	
		self.tagComponents, self.tagList = [], {}
		self.tagComponents.append(self.textbox)

		imgFileNames = self.model.getFiles()
		self.tagList = {key: val for key, val in enumerate(imgFileNames)}
		# for i in range(len(imgFileNames)):
		# 	self.tagList.append(i)
		# # self.tagList.append(imgFileNames)

		# # TODO: add this stuff into the Model so that each Model (QLabel)
		# tagFileNames = os.listdir('tags')
		# for f in tagFileNames:
		# 	file = open('tags/' + f, 'r')
		# 	fNameNoExt = f[0:f.find('.txt')]
		# 	for imgName in imgFileNames:
		# 		if imgName == fNameNoExt:
		# 			for tag in file.readlines():
		# 				index = imgFileNames.index(imgName)
		# 				# self.tagList.append(list(range(len(imgFileNames))))
		# 				self.tagList[index].append(tag)								
		# 				# self.tagList[fNameNoExt].append(tag)			
		print(self.tagList)

	# add textbox, buttons, and tags
	def showTagComponents(self):
		padding = self.model.getFullBorder()
		windowWidth = self.model.getWindowWidth()
		windowHeight = self.model.getWindowHeight()
		self.textbox.resize(windowWidth/3, padding)
		self.textbox.move(padding, windowHeight - padding*2)
		self.textbox.setStyleSheet('border: 1px solid #868e96;')
			
		# connect button to function on_click
		self.addButton = QPushButton('Add Tag', self)
		self.saveButton = QPushButton('Save All Tags', self)
		self.addButton.clicked.connect(self.addTag)
		self.saveButton.clicked.connect(self.saveTags)
		self.addButton.setStyleSheet('background-color: #868e96;')
		self.saveButton.setStyleSheet('background-color: #868e96;')

		# self.addButton.setStyleSheet("background-color: rgb(0, 128, 128)")
		self.addButton.move(windowWidth/2, windowHeight - padding*2)
		self.saveButton.move(windowWidth/1.5, windowHeight - padding*2)

		self.tagComponents.append(self.addButton)
		self.tagComponents.append(self.saveButton)
		for t in self.tagComponents:
			t.show()

		# print()
	def hideTagComponents(self):
		for t in self.tagComponents:
			t.hide()

	def saveTags(self):
		print()

	def addTag(self):
		# get new tag from QLineEdit
		textBoxStr = self.textBox.text()
		myTagList = self.tagList[self.model.currImage]
		# add to list of tags for current image
		myTagList.append(textBoxStr)
		self.updateCurrentTags(myTagList)
		self.updateCurrentTagsButtons(myTagList)

		self.textBox.setText()
		self.setFocus()

	def updateCurrentTags(self, mtl):
		ss = 'something tag: '
		for s in mtl:
			ss = ss + ' ' + s
		print('Tag list: ', ss)
		self.currentTags.setText(ss)
		#self.curentTags.show()

	def updateCurrentTagsButtons(self, mtl):
		print(mtl)

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
		# self.sound.play()	
		
	# Full screen mode on clicked label while in thumbnail mode
	def mouseSel(self, label, testStr):
		if self.model.getMode() == 0:
			self.model.setMode(1)
			self.model.setSelectedIndex(label.getPixIndex())
		self.setFocus()
		self.draw()		

	def mouseClickEvent(self, event):
		print('here')
	
	# TODO: Bugfix
	# Handles key events and responds according to current browser state
	def keyPressEvent(self, event):
		up, down, left, right = 16777235, 16777237, 16777234, 16777236
		scrollL, scrollR = 44, 46
		thumb, full = 0, 1
		short, medium, big = 0, 1, 2
		tab, esc = 16777217, 16777216
		currentMode = self.model.getMode()

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
			#print('Left move. New Index: '+str(newIndex))
			if newIndex < leftmost or newIndex > selected:
				self.model.setLeftmostIndex(leftmost - 5)
			# elif ():
			self.model.setSelectedIndex(newIndex)
			self.playSound(short)
		# Right - Thumbnail		
		elif currentMode == thumb and event.key() == right:
			selected = self.model.getSelectedIndex()
			leftmost = self.model.getLeftmostIndex()
			newIndex = (selected + 1) % len(self.model.getFiles())
			# TODO: bugfix - moving right when left > newIndex
			if newIndex > ((leftmost + 4) % len(self.model.getFiles())):
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

		# print('Leftmost: '+str(self.model.getLeftmostIndex())+'\tSelected: '+str(self.model.getSelectedIndex()))

		self.draw()

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(6):
			# self.labels[i].setStyleSheet('border: none')
			self.labels[i].hide()


