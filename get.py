#!/usr/bin/env python3

import sys
from pystalkd.Beanstalkd import SocketError
from connection import ArchiverConnection
import archivejob
import backup
import settings
import json
from time import sleep


#
# main
#
setup = settings.beanstalkd

try:
    c = ArchiverConnection(*setup['connection'])
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

b = backup.Backup()

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
        archiveJob = json.loads(job.body, cls=archivejob.ArchiveJobDecoder)
        archiveJob.setChecksum()
        if b.run(archiveJob):
            print("Success backuping file {} from {}".format(archiveJob.filename, archiveJob.host))
            job.delete()
        else:
            print("Error while backuping file {} from {}".format(archiveJob.filename, archiveJob.host))
            job.release()

    sleep(setup['timeout'])
