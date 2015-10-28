#!/usr/bin/env python3

from archiver.connection import Connection
from archiver.backup import Backup
from archiver.job import Job, JobEncoder
from pystalkd.Beanstalkd import Connection
import json
import hashlib
import settings

setup = settings.beanstalkd


c = Connection(*setup['connection'])

c.use(setup['tubes']['use'])
print("Using tube {}".format(c.using()))

jobs = []

filename = "/tmp/test.log"
backup = Job("localhost", filename)
backup.setChecksum()

jobs.append(backup)

for job in jobs:
	body = json.dumps(backup, cls=JobEncoder)
	print(body)
	c.put(body)
