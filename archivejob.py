#!/usr/bin/env/python3

from datetime import datetime
import hashlib
import json
import subprocess
import sys, os, errno
import settings


class ArchiveJob:
	def __init__(self, host, filename):
		'''
		:param host: string with a fqdn hostname
		:param filename: string containing a full path to a file
		:return: boolean
		'''
		self.host = host
		self.filename = filename
		if not os.path.isfile(self.filename):
			raise ValueError("Invalid filename")
		self.checksum = None
		self.date = datetime.now().timestamp()


	def calculateChecksum(self, filename):
		'''
		Calculates a md5 hash
		:param filename: string containing a full path to a file
		:return: boolean
		'''
		hash = hashlib.md5()

		try:
			file = open(filename, 'rb')
			while True:
				data = file.read(128) # as recommended in doc
				if not data:
					break
				hash.update(data)
		except:
			return False

		return hash.hexdigest()


	def setChecksum(self):
		self.checksum = self.calculateChecksum(self.filename)


	def __str__(self):
		return "{} :: {} :: {}".format(self.host, self.filename, self.date)




class ArchiveJobEncoder(json.JSONEncoder):
	def default(self, object):
		if isinstance(object, ArchiveJob):
			return object.__dict__
		return json.JSONEncoder.default(self, object)



class ArchiveJobDecoder(json.JSONDecoder):
	def decode(self, string):
		data = json.JSONDecoder.decode(self, string)
		return ArchiveJob(data['host'], data['filename']);
