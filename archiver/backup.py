#!/usr/bin/env/python3

import subprocess
import sys, os, errno
import settings
from .job import Job

class Backup:
	def buildTargetFolder(self, host, sourceFolder, targetFolder):
		'''
		Tries to execute mkdir -p to create the target folder /targetFolder/host/folder path
		and returns a string containing built folder
		:param host: string with a fqdn hostname
		:param sourceFolder: string containing a full path of the source folder on specified host
		:param targetFolder: string containing a full path to a destinatino folder
		:return targetFolder: string containing the folder where backup will be saved
		''' 
		targetFolder = '{}/{}{}'.format(targetFolder, host, sourceFolder)
		try:
			os.makedirs(targetFolder)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(targetFolder):
				pass
			else: raise

		return targetFolder


	def scp(self, user, host, sourceFilename, targetFilename, logFile=None, logError=None):
		'''
		Copy a remote file on host to local filesystem via ssh
		:param user: ssh login
		:param host: remote host where file is located
		:param sourceFilename: full path of file to be copied
		:param targetFilename: full path of the new file on local filesystem
		:param logFile: full path of the file for stdout messages
		:param logError: full path of the file for stderr messages
		:return: boolean
		''' 
		accessLog = open(logFile, 'w')
		errorLog = open(logError, 'w')
		command = "rsync -avz {}@{}:{} {}"
		cmd = command.format(user, host, sourceFilename, targetFilename)
		proc = subprocess.Popen(cmd.split(), stdout = accessLog, stderr = errorLog)
		while True:
			if proc.poll() is not None:
				if proc.returncode > 0:
					raise Exception('An error ocurred while copying the file.')
					return False
				break
		accessLog.close()
		errorLog.close()
		return True


	def isChecksumCorrect(self, job1, job2):
		'''
		Compare two job checksums
		:param job1: Job
		:param job2: Job
		:return: boolean
		'''
		return job1.checksum == job2.checksum


	def run(self, job):
		'''
		Do a backup using job information
		:param job: Job
		:return: boolean
		'''
		sourceFolder, targetFilename = os.path.split(job.filename)
		targetFolder = self.buildTargetFolder(job.host, sourceFolder, settings.targetFolder)
		targetFilename = '{}/{}'.format(targetFolder, targetFilename)
		user = settings.sources[job.host]['user']

		if not os.path.isfile(targetFilename):
			print("Copying file from {}".format(job.host))
			try:
				self.scp(user, job.host, job.filename, targetFilename, settings.logFile['stdout'], settings.logFile['stderr'])
			except:
				raise Exception('Unknown error while copying the file, check log files.')
				sys.exit(3)

		expectedJob = Job(None, targetFilename)
		expectedJob.setChecksum()

		return self.isChecksumCorrect(job, expectedJob)
