from models import *
from django.http import HttpResponse
import datetime
def backupDatabase(request):
	pass

def notificationTrigger(request):
	targetList = Student.objects.filter(balance__range=(0, 10))
	mailList = []
	output = ''
	for eachStudent in targetList:
		mailList += [eachStudent.emailid]
		output += eachStudent.firstname + '<br>'
	subject = 'Recharge your IOESTS balance'
	message = '''Dear Student,
	Your IOESTS account balance is getting low. Please recharge your account.
	Thanks
	'''
	return HttpResponse(sendEmail(subject = subject, message = message, mailingList = mailList))

from django.db import connection
def accountingTask(request):
	# totalTrans = Activity.objects.all()
	totalTrans = Activity.objects.getTodaysActivity()
	# totalTrans = [row for row in cursor.fetchone()]
	# totalTrans = Activity.objects.filter(date = datetime.date.today())
	output = '<html>this is test'
	totalDeposit, totalCredit = 0, 0
	for trans in totalTrans:
		output += str(trans[0]) +  '<br />'
		if (trans[2] == 'credit deposited'):
			totalDeposit += trans[5]
		elif (trans[2] == 'credit withdrawed'):
			totalCredit += trans[5]
		elif (trans[2] == 'payment'):
			totalCredit += trans[5]
	output += '''<br /> Total deposit amount = %d<br />
						Total return amount = %d<br />
						Total Transaction amount = %d
				''' % (totalDeposit, totalCredit, totalDeposit + totalCredit)
	output += '</html>'
	return HttpResponse(output)


from django.core.mail import send_mail
def sendEmail(subject, message, mailingList = []):
	if mailingList:
		send_mail(
				subject,
				message,
				'ioests.noreply@gmail.com',
				mailingList,
			)
		return True
	return False