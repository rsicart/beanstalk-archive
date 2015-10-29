#!/usr/bin/env python3

import sys
from pystalkd.Beanstalkd import SocketError
from archiver.connection import Connection
from archiver.backup import Backup
from archiver.job import Job, JobDecoder
import settings
import json
from time import sleep


#
# main
#
setup = settings.beanstalkd

try:
    c = Connection(*setup['connection'])
    c.watchMany(setup['tubes']['watch'])
    c.ignoreMany(setup['tubes']['ignore'])
    print("Watching tubes {}".format(c.watching()))
    print("Ignoring tubes {}".format(setup['tubes']['ignore']))
except ConnectionRefusedError as e:
    print(e)
    sys.exit(1)
except SocketError as e:
    print(e)
    sys.exit(1)

b = Backup()

while True:

    if c.isBroken():
        try:
            c.reconnect()
            c.watchMany(setup['tubes']['watch'])
            c.ignoreMany(setup['tubes']['ignore'])
        except ConnectionRefusedError as e:
            print(e)
            sys.exit(3)
        except SocketError as e:
            print(e)
            sys.exit(4)

    job = c.reserve(setup['timeout'])

    if job:
        archiverJob = json.loads(job.body, cls=JobDecoder)
        if b.run(archiverJob):
            print("Success backuping file {} from {}".format(archiverJob.filename, archiverJob.host))
            job.delete()
        else:
            print("Error while backuping file {} from {}".format(archiverJob.filename, archiverJob.host))
            job.release()

    sleep(setup['timeout'])
