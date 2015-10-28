#!/usr/bin/env python3

targetFolder = '/tmp'

sources = {
	'localhost': {
		'user':'root',
    },
	'127.0.0.1': {
		'user':'root',
    }
}

logging = True
logFile = {
    'stdout': '/tmp/beanstalk-archiver.log',
    'stderr': '/tmp/beanstalk-archiver.log',
}
