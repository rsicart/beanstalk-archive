#!/usr/bin/env python3

from archiver.connection import Connection
from archiver.backup import Backup
from archiver.job import Job, JobDecoder
from archiver.alert import Email
from daemonize import Daemonize
from datetime import datetime
from pystalkd.Beanstalkd import SocketError
from time import sleep
import json
import logging
import settings
import socket
import sys

pid = "/tmp/archiver-worker.pid"

# logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler(settings.logFile['stdout'], 'w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def send_alert(error):
	if settings.alerts['enabled']:
		alerts = []
		msg = 'An error ocurred during "{}" execution.\nPlease, connect to host "{}" and check the process logs.\n'.format(__file__, socket.getfqdn())
		alert = Email(settings.alerts['email']['server'], settings.alerts['email']['port'], settings.alerts['email']['sender'], ', '.join(settings.alerts['email']['recipients']), msg)
		alert.send()


# action setup for daemon
def main():
	setup = settings.beanstalkd

	try:
		c = Connection(*setup['connection'])
		c.watchMany(setup['tubes']['watch'])
		c.ignoreMany(setup['tubes']['ignore'])
		logger.info("Watching tubes {}".format(c.watching()))
		logger.info("Ignoring tubes {}".format(setup['tubes']['ignore']))
	except ConnectionRefusedError as e:
		logger.error(e)
		send_alert(e)
		sys.exit(1)
	except SocketError as e:
		logger.error(e)
		send_alert(e)
		sys.exit(1)

	b = Backup()

	while True:

		if c.isBroken():
			try:
				c.reconnect()
				c.watchMany(setup['tubes']['watch'])
				c.ignoreMany(setup['tubes']['ignore'])
			except ConnectionRefusedError as e:
				logger.error(e)
				send_alert(e)
				sys.exit(3)
			except SocketError as e:
				logger.error(e)
				send_alert(e)
				sys.exit(4)

		job = c.reserve(setup['timeout'])

		if job:
			archiverJob = json.loads(job.body, cls=JobDecoder)
			if b.run(archiverJob):
				logger.info("Success backuping file {} from {}".format(archiverJob.filename, archiverJob.host))
				job.delete()
			else:
				logger.info("Error while backuping file {} from {}".format(archiverJob.filename, archiverJob.host))
				job.release()

		sleep(setup['timeout'])



daemon = Daemonize(app="ArchiverWorker", pid=pid, action=main, keep_fds=keep_fds)
daemon.start()
