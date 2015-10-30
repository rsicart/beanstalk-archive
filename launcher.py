#!/usr/bin/env python3

import os
import settings


# setup virtualenv
virtualenv_folder = os.path.expanduser(settings.virtualenvFolder)
virtualenv_activate = os.path.join(virtualenv_folder, 'bin/activate_this.py')
try:
	exec_namespace = dict(__file__=virtualenv_activate)
	with open(virtualenv_activate, 'rb') as exec_file:
	  file_contents = exec_file.read()
	compiled_code = compile(file_contents, virtualenv_activate, 'exec')
	exec(compiled_code, exec_namespace)
except IOError:
	pass

# launch worker
script = "./beanstalk-archiver-worker.py"
os.execl(script, '')
