#!/usr/bin/env python3

import settings
import smtplib
from email.mime.text import MIMEText

class Alert:
	def __init__(self, target, msg):
		self.target = target
		self.msg = msg
	
	def send(self):
		raise NotImplementedError


class Email(Alert):
	def __init__(self, smtp_server, smtp_port, sender, target, msg):
		super().__init__(target, msg)
		self.smtp_server = smtp_server
		self.smtp_port = smtp_port
		self.sender = sender

	def send(self):
		msg = MIMEText(self.msg)
		msg['Subject'] = ''
		msg['From'] = self.sender
		msg['To'] = self.target
		s = smtplib.SMTP(self.smtp_server, self.smtp_port)
		s.send_message(msg)
		s.quit()
