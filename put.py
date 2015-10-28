#!/usr/bin/env python3

from pystalkd.Beanstalkd import Connection
import archiverjob
import json
import hashlib
import settings

setup = settings.beanstalkd


c = Connection(*setup['connection'])

c.use(setup['tubes']['use'])
print("Using tube {}".format(c.using()))

jobs = []

filename = "/tmp/test.log"
backup = archiverjob.ArchiverJob("localhost", filename)
backup.setChecksum()

jobs.append(backup)

for job in jobs:
	body = json.dumps(backup, cls=archiverjob.ArchiverJobEncoder)
	print(body)
	c.put(body)
