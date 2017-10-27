# pip3 install twisted

from twisted.internet import defer
from twisted.python import failure, util
from PyQt5 import QtNetwork, QtCore

class ImageFetcher():

	def __init__(self, nam, url):
		self.nam = nam
		self.request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
		self.reply = self.nam.get(self.request)
		self.reply.finished.connect(self._handle)
		self.d = defer.Deferred()

	def _handle(self, test):
		# do stuff with self.reply()
		print(test, 'in _handle')
		er = self.reply.error()
		if er == QtNetwork.QNetworkReply.NoError:
			print('no error')
			result = self.reply.readAll() # something really cool ...
			self.d.callback(result)
			# self.reply.deleteLater()

	def getPromise(self):
		return self.d