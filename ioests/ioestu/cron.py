from django_cron import cronScheduler, Job

from ioestu.endofday import *

class CheckMail(Job):
	"""
	Cron Job that checks the lgr users mailbox and adds any 
	approved senders' attachments to the db
	"""

	# run every 300 seconds (5 minutes)
	run_every = 300
		
	def job(self):
		backupDatabase()

cronScheduler.register(CheckMail)