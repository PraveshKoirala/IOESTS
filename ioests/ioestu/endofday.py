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
		mailList += [eachStudent.firstname]
		output += eachStudent.firstname + '<br>'
	return HttpResponse(output)

def accountingTask(request):

	# totalTrans = Activity.objects.all()
	totalTrans = Activity.objects.all()
	output = '<html>'
	for item in totalTrans:
		output += item.type+"<br>"
	output += '</html>'
	return HttpResponse('today is' + datetime.datetime.date)