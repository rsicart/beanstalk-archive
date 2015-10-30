#!/usr/bin/env python3

virtualenvFolder = "~/virtualenvs/beanstalk"

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

beanstalkd = {
    'connection': ('localhost', 11301),
    'tubes': {
        'watch': ['myTube'],
		'use': 'myTube',
        'ignore': ['default'],
    },
    'timeout': 300,
}
