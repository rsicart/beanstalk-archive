#!/usr/bin/env python3

import pystalkd

class Connection(pystalkd.Beanstalkd.Connection):

	def isBroken(self):
		sent = self._socket.send(b'archiver ping\r\n')
		chunk = self._socket.recv(128)
		if sent == 0 or len(chunk) == 0:
			return True
		return False


	def watchMany(self, tubes):
		for tube in tubes:
			self.watch(tube)


	def ignoreMany(self, tubes):
		for tube in tubes:
			self.ignore(tube)
