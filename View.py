 # File: ImageBrowser.py, Model.py, View.py
# By: Steve Pedersen
# Date: September 25, 2017
# Usage: python3 ImageBrowser.py 
# System: OS X
# Dependencies: Python3, PyQt5, requests (pip3 install requests)
# Description: Creates a Model to keep track of current state of data in View
#		Also, displays images, handles user events, tag actions, etc..

import Model, os, sys, json, requests, time
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QAction, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSoundEffect

class View(QWidget):

	WINDOW_TITLE = 'Image Browser'
	THUMB_QTY = 5
	WINDOW_STYLE = 'background-color: #FFFFFF;'
	BUTTON_STYLE = 'background-color: #d3d3d3; padding: 8px 20px; font-weight: bold;'
	FLICKR_URL = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&nojsoncallback=1'
	TEST_URLS = ['http://www.eatwisconsincheese.com/images/cheese/Limburger-h.jpg',
		'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Hot_dog_with_mustard.png/1200px-Hot_dog_with_mustard.png',
		'https://aff5fa4925746bf9c161-fb36f18ca122a30f6899af8eef8fa39b.ssl.cf5.rackcdn.com/images/Masthead_mario.17345b1513ac044897cfc243542899dce541e8dc.9afde10b.png']

	def __init__(self, windowWidth, files):
		super().__init__()
		self.title = View.WINDOW_TITLE
		self.model = Model.Model(self)
		self.model.setThumbQty(View.THUMB_QTY)
		self.model.initModel(windowWidth, files)
		self.labels = self.model.generateLabels(self, View.THUMB_QTY + 1)
		self.api_key = '56cd9cd52b1e025a3684840a4176cf88'
		self.initUI()
		self.show()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(0, 0, self.model.getWindowWidth(), self.model.getWindowHeight())
		self.setStyleSheet(View.WINDOW_STYLE)	
		self.showThumbModeComponents()
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
			y = self.model.getWindowHeight() - (self.model.getThumbHeight() * 3) 
			y = y if y < self.model.getWindowHeight() - 150 else self.model.getWindowHeight() - 250
			for i in range(View.THUMB_QTY):
				x = int(((self.model.getWindowWidth() - self.model.getThumbWidth()*View.THUMB_QTY)/2) + i*self.model.getThumbWidth())
				# Center the highlighted thumbnail when returning from full screen mode
				thumb = (leftmost + i) % self.model.getImageCount()				
				color = 'green'
				if thumb == selected:
					color = 'red'	
				
				self.attachPixmap(thumb, i, x, y, self.model.getThumbWidth(), self.model.getThumbHeight(), self.model.getThumbBorder(), color)
			self.hideFullModeComponents()
			self.hideTags()
			self.showThumbModeComponents()

		# Full Screen Mode		
		elif mode == 1:
			x = (self.model.getWindowWidth() - self.model.getFullWidth()) / 2
			y = (self.model.getWindowHeight() - self.model.getFullHeight()) / 2
			self.attachPixmap(selected, View.THUMB_QTY, x, y, self.model.getFullWidth(), self.model.getFullHeight(), self.model.getFullBorder(), 'red')
			self.showFullModeComponents()
			self.showTags()

	# Assigns an image to one of the labels
	def attachPixmap(self, pindex, lindex, x, y, w, h, b, color):
		#print(pindex, lindex, x, y, w, h, b, color)
		mode = 0
		if lindex == View.THUMB_QTY:
			mode = 1

		self.labels[lindex].setPixIndex(pindex)
		self.labels[lindex].setPixmap(self.model.getPixmap(mode, pindex))
		self.labels[lindex].setAlignment(Qt.AlignCenter)
		self.labels[lindex].setGeometry(QRect(x, y, w, h))
		self.labels[lindex].setStyleSheet('border: ' + str(b) + 'px solid '+ color)
		self.labels[lindex].clicked.connect(self.mouseSel)
		self.labels[lindex].show()

	def showThumbModeComponents(self):
		windowWidth = self.model.getWindowWidth()
		windowHeight = self.model.getWindowHeight()	
		padding = windowWidth / 25 if windowWidth / 25 < 35 else 35

		self.thumbModeComponents = []
		self.searchTextBox = QLineEdit(self)	
		self.searchTextBox.resize(windowWidth/3, padding*1.5)
		self.searchTextBox.move(padding, windowHeight - padding*4)
		self.searchTextBox.setStyleSheet('border: 1px solid #868e96;')	
		self.searchTextBox.setPlaceholderText('Search Flickr...')
		self.maxResultBox = QLineEdit(self)	
		self.maxResultBox.resize(windowWidth/20, padding*1.5)
		self.maxResultBox.move(windowWidth/1.6, windowHeight - padding*4)
		self.maxResultBox.setStyleSheet('border: 1px solid #868e96;')	
		self.maxResultBox.setText('10')
		self.maxResultLabel = QLabel(self)
		self.maxResultLabel.resize(windowWidth/6, padding*1.5)
		self.maxResultLabel.move(windowWidth/1.45, windowHeight - padding*4)
		self.maxResultLabel.setText('Max Search Results')

		self.searchButton = QPushButton('Search', self)
		self.searchButton.clicked.connect(self.search)
		self.searchButton.setStyleSheet(View.BUTTON_STYLE)
		self.searchButton.move(windowWidth/2.5, windowHeight - padding*3.8)
		self.testButton = QPushButton('Test', self)
		self.testButton.clicked.connect(self.test)
		self.testButton.setStyleSheet(View.BUTTON_STYLE)
		self.testButton.resize(padding*2.6, padding)
		self.testButton.move(padding, windowHeight - padding*2)
		self.saveAllButton = QPushButton('Save', self)
		self.saveAllButton.clicked.connect(self.saveAll)
		self.saveAllButton.setStyleSheet(View.BUTTON_STYLE)
		self.saveAllButton.resize(padding*2.6, padding)
		self.saveAllButton.move(padding+padding*2.6, windowHeight - padding*2)
		self.exitButton = QPushButton('Exit', self)
		self.exitButton.clicked.connect(self.exit)
		self.exitButton.setStyleSheet(View.BUTTON_STYLE)
		self.exitButton.resize(padding*2.6, padding)
		self.exitButton.move(padding+2*padding*2.6, windowHeight - padding*2)
		self.deleteButton = QPushButton('Delete', self)
		self.deleteButton.clicked.connect(self.delete)
		self.deleteButton.setStyleSheet(View.BUTTON_STYLE)
		self.deleteButton.resize(padding*2.6, padding)
		self.deleteButton.move(padding+3*padding*2.6, windowHeight - padding*2)

		self.statusText = QLabel(self)
		self.statusText.resize(windowWidth-padding*2, padding)
		self.statusText.move(padding, windowHeight - padding)		

		self.thumbModeComponents.append(self.searchTextBox)
		self.thumbModeComponents.append(self.searchButton)
		self.thumbModeComponents.append(self.maxResultBox)
		self.thumbModeComponents.append(self.maxResultLabel)
		self.thumbModeComponents.append(self.testButton)
		self.thumbModeComponents.append(self.saveAllButton)
		self.thumbModeComponents.append(self.exitButton)
		self.thumbModeComponents.append(self.deleteButton)
		self.thumbModeComponents.append(self.statusText)
		for t in self.thumbModeComponents:
			t.show()

	# NOTE: requires requests module to be installed
	# https://farm{farm-id}.staticflickr.com/{server-id}/{id}_{o-secret}.(jpg|gif|png)
	def test(self):
		query = self.searchTextBox.text()
		query = query.replace(' ', '%20')
		url = self.FLICKR_URL + '&per_page=1&api_key='+self.api_key + '&tags='+query
		response = requests.get(url).json()
		if (response['stat'] == 'ok'):
			pj = response['photos']['photo'][0]
			photoUrl = 'https://farm'+str(pj['farm'])+'.staticflickr.com/'+str(pj['server'])+'/'+str(pj['id'])+'_'+str(pj['secret'])+'.jpg'
			fileNames = self.model.requestImages([photoUrl])
			self.addToTagDict(fileNames)
			self.model.addFiles(fileNames)					
		else:
			self.statusText.setText('No results found.')

	def saveAll(self):
		print()
	def exit(self):
		sys.exit()
	def delete(self):
		print()

	def hideThumbModeComponents(self):
		for t in self.thumbModeComponents:
			t.hide()
			# t.setVisible(False)

	# TODO: Make this actually use search query from textbox to ping the Flickr API
	def search(self):
		query = self.searchTextBox.text()
		query = query.replace(' ', '%20')
		maxResults = self.maxResultBox.text() if len(self.maxResultBox.text()) > 0 else '1'
		url = self.FLICKR_URL + '&per_page='+maxResults + '&api_key='+self.api_key + '&tags='+query
		response = requests.get(url).json()
		if (response['stat'] == 'ok'):
			photoUrls = []
			for p in response['photos']['photo']:
				photoUrl = 'https://farm'+str(p['farm'])+'.staticflickr.com/'+str(p['server'])+'/'+str(p['id'])+'_'+str(p['secret'])+'.jpg'
				photoUrls.append(photoUrl)
			fileNames = self.model.requestImages(photoUrls)
			self.addToTagDict(fileNames)
			self.model.addFiles(fileNames)					
		else:
			self.statusText.setText('No results found.')		
		
		# fileNames = self.model.requestImages(View.TEST_URLS)
		# self.addToTagDict(fileNames)
		# self.model.addFiles(fileNames)
		# self.draw()
		# self.initTags()

	def addToTagDict(self, items):
		for item in items:
			self.tagDict.update( { item: [] } )	

	# Pre-load all tags for each image into a dictionary
	def initTags(self):
		self.tagTextBox = QLineEdit(self)	
		self.fullModeComponents, self.tagDict = [], {}
		self.fullModeComponents.append(self.tagTextBox)
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
			self.tags[i].setStyleSheet(View.BUTTON_STYLE)
			self.tags[i].move(padding/4, padding + padding*i*1.4)
			self.tags[i].show()

	def hideTags(self):
		for t in self.tags:
			t.hide()
			t.setVisible(False)
		self.tags = []


	# Add textbox, buttons, and tags
	def showFullModeComponents(self):
		padding = 30
		windowWidth = self.model.getWindowWidth()
		windowHeight = self.model.getWindowHeight()

		self.tagTextBox.resize(windowWidth/3, padding*1.5)
		self.tagTextBox.move(padding, windowHeight - padding*2)
		self.tagTextBox.setStyleSheet('border: 1px solid #868e96;')
		self.tagTextBox.setPlaceholderText('Enter tag text...')

		# connect button to functions add/saveTags
		self.addButton = QPushButton('Add Tag', self)
		self.saveTagsButton = QPushButton('Save All Tags', self)
		self.addButton.clicked.connect(self.addTag)
		self.saveTagsButton.clicked.connect(self.saveTags)
		self.addButton.setStyleSheet(View.BUTTON_STYLE)
		self.saveTagsButton.setStyleSheet(View.BUTTON_STYLE)

		self.addButton.move(windowWidth/2, windowHeight - padding*1.7)
		self.saveTagsButton.move(windowWidth/1.5, windowHeight - padding*1.7)

		self.fullModeComponents.append(self.addButton)
		self.fullModeComponents.append(self.saveTagsButton)
		for t in self.fullModeComponents:
			t.show()

	def hideFullModeComponents(self):
		for t in self.fullModeComponents:
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
			newIndex = (selected - 1) % self.model.getImageCount()
			if selected == leftmost:
				self.model.setLeftmostIndex(leftmost - View.THUMB_QTY)
			self.model.setSelectedIndex(newIndex)
			self.playSound(short)
		# Right - Thumbnail		
		elif currentMode == thumb and event.key() == right:
			selected = self.model.getSelectedIndex()
			leftmost = self.model.getLeftmostIndex()
			newIndex = (selected + 1) % self.model.getImageCount()
			if selected == ((leftmost + View.THUMB_QTY - 1) % self.model.getImageCount()):
				self.model.setLeftmostIndex(leftmost + View.THUMB_QTY)
			self.model.setSelectedIndex(newIndex)
			self.playSound(short)
		# Next set Left - Thumbnail		
		elif currentMode == thumb and event.key() == scrollL:
			selected = self.model.getSelectedIndex()
			newIndex = (selected - View.THUMB_QTY) % self.model.getImageCount()
			self.model.setSelectedIndex(newIndex)
			self.model.setLeftmostIndex(newIndex)
			self.playSound(big)
		# Next set Right - Thumbnail		
		elif currentMode == thumb and event.key() == scrollR:
			selected = self.model.getSelectedIndex()
			newIndex = (selected + View.THUMB_QTY) % self.model.getImageCount()
			self.model.setSelectedIndex(newIndex)
			self.model.setLeftmostIndex(newIndex)
			self.playSound(big)
		elif currentMode == full and event.key() == enter:
			self.addTag()

		# print('Leftmost: '+str(self.model.getLeftmostIndex())+'\tSelected: '+str(self.model.getSelectedIndex()))
		self.draw()

	# Hide any visible contents on browser window
	def clearBrowser(self):
		for i in range(View.THUMB_QTY + 1):
			self.labels[i].hide()
		self.hideTags()
		self.hideThumbModeComponents()
		# self.hideFullModeComponents()

