from models import *
from django.http import HttpResponse
import datetime
def backupDatabase(request):
	pass

def notificationTrigger(request):
	targetList = Student.objects.filter(balance = 0)
	mailList = []
	output = ''
	for eachStudent in targetList:
		mailList += [eachStudent.emailid]
		output += eachStudent.firstname + '<br>'
	subject = 'Recharge your IOESTS balance'
	message = '''Dear Student,
	Your IOESTS account balance has been credited to Rs. 0.00. Please recharge your account.
	Thanks
	'''
	return HttpResponse(sendEmail(subject = subject, message = message, mailingList = mailList))

def accountingTask(request):
	# totalTrans = Activity.objects.all()
	totalTrans = Activity.objects.all()
	output = '<html>'
	for item in totalTrans:
		output += item.type+"<br>"
	output += '</html>'
	return HttpResponse('today is' + datetime.datetime.date)

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