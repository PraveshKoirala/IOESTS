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
	cursor = connection.cursor()
	cursor.execute('''
			select * from ioestu_activity 
			where date between now()- interval '1 days' + interval '+5:45' HOUR TO MINUTE and now() + interval '+5:45' HOUR TO MINUTE
		''')
	# totalTrans = [row for row in cursor.fetchone()]
	# totalTrans = Activity.objects.filter(date = datetime.date.today())
	output = '<html>this is test'
	for item in cursor:
		output += str(item[6])+"<br>"
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