# Requirements

* a beanstalkd server up and running
* python3
* pyyaml
* pystalkd
* daemonize

# Optional

* a smtp server to send email alerts

# Get started

1. Create a virtualenv and install dependencies:
```
virtualenv -p /usr/bin/python3 ~/.virtualenvs/beanstalk-archive
source ~/.virtualenvs/beanstalk-archive/bin/activate
pip install pyyaml pystalkd daemonize
```

2. Go to repository folder and create a settings file
```
cp settings.example.py settings.py
```

3. Configure `settings.py` with your environment settings

4. Finally, you can launch:
* `get.py` to see a sample script execution in foreground
* `beanstalk-archive-worker.py` to begin job treatment in background (when your virtualenv is active)
* `launcher.py` to begin job treatment in background (when your virtualenv is NOT active, launcher will activate the virtualenv itself)

# Tips

When beanstalkd service is running on a different machine than the worker (aka consumer), you have 2 options:

a) setup beanstalk to listen on a public interface and setup a firewall rule to accept only desired connections
b) setup a SSH tunnel from worker to beanstalkd server

Option *B* is easier to set up. As an example, on worker machine, execute this command:
```
ssh -N -L11301:localhost:11300 toto@beanstalkd.example.com &
```

Now, update `settings.py` to connect to beanstalkd via our new tunnel:
```
beanstalkd = {
    'connection': ('localhost', 11301),
	...
}
```

Note: you need ssh access to `beanstalkd.example.com` to successfully create the tunnel.
