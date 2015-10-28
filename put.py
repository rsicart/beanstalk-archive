#!/usr/bin/env python3

from pystalkd.Beanstalkd import Connection
import archivejob
import json
import hashlib
import settings

setup = settings.beanstalkd


c = Connection(*setup['connection'])

c.use(setup['tubes']['use'])
print("Using tube {}".format(c.using()))

jobs = []

filename = "/tmp/test.log"
backup = archivejob.ArchiveJob("localhost", filename)
backup.setChecksum()

jobs.append(backup)

for job in jobs:
	body = json.dumps(backup, cls=archivejob.ArchiveJobEncoder)
	print(body)
	c.put(body)
