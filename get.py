#!/usr/bin/env python3

import sys
from pystalkd.Beanstalkd import Connection, SocketError
import archivejob
import backup
import settings
import json
from time import sleep

setup = settings.beanstalkd

def isActiveSocket(socket):
    sent = socket.send(b'ping\r\n')
    chunk = socket.recv(128)
    if sent == 0 or len(chunk) == 0:
        return False
    return True


# main

try:
    c = Connection(*setup['connection'])
except ConnectionRefusedError as e:
    print(e)
    sys.exit(1)
except SocketError as e:
    print(e)
    sys.exit(1)

for tube in setup['tubes']['watch']:
    c.watch(tube)

for tube in setup['tubes']['ignore']:
    c.ignore(tube)

print("Watching tubes {}".format(c.watching()))
print("Ignoring tubes {}".format(setup['tubes']['ignore']))

b = backup.Backup()

while True:

    if not isActiveSocket(c._socket):
        try:
            c.reconnect()
            for tube in setup['tubes']['watch']:
                c.watch(tube)
            for tube in setup['tubes']['ignore']:
                c.ignore(tube)
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
