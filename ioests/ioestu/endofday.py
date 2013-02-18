from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from emailTemplates import *
import json
import os.path

def getJson(data):
	dataList = []
	for item in data:
		dataList.append({
					'id' : str(item[0]),
					'student' : item[1],
					'atype' : item[2],
					'operator' : item[3],
					'detail': item[4],
					'amount': item[5],
					'date' : str(item[6]), 
		})
	return json.dumps(dataList)

def backupDatabase(request = None):
	totalTrans = Activity.objects.getTodaysActivity()
	jsonData = getJson(totalTrans)
	
	fileName = 'activityBackup/backup'+str(datetime.date.today())+'.sts'
	backupFile = open(fileName, 'w+')
	backupFile.write(jsonData)
	backupFile.close()
	
	return True


def notificationTrigger(request = None):
	targetList = Student.objects.filter(balance__range=(0, 10))
	mailList = []
	for eachStudent in targetList:
		mailList += [eachStudent.emailid]
	sendEmail(subject = rechargeSubject, message = rechargeMessage, mailingList = mailList)
	return True


def accountingTask(request = None):		#type of transaction left to be filled
	totalTrans = Activity.objects.getTodaysActivity()
	totalDeposit, totalCredit, output = 0, 0, ''
	
	for trans in totalTrans:
		if (trans[2] == 'deposit'):
			totalDeposit += trans[5]
		elif (trans[2] == 'payment'):
			totalCredit += trans[5]
	netDeposit = totalDeposit - totalCredit
	
	if balanceSheet.objects.all():
		lastEntry = balanceSheet.objects.all().order_by('-date')[0]
		if lastEntry.date != datetime.date.today():
			netDeposit += lastEntry.netBalance
	
	balance = balanceSheet(
		incoming = totalDeposit,
		 outgoing = totalCredit, 
		 date = datetime.date.today(), 
		 netBalance = netDeposit)
	balance.save()
	
	sendEmail(reportSubject, getReportMessage(totalDeposit, totalCredit), EMAIL_SUPERUSER)
	
	return True


########## only admin should be accessible to this routine
def endOfDayEvents(request):
	message = {}
	
	if request.method == "POST":
		accountingTask()
		backupDatabase()
		notificationTrigger()


	transactionToday = balanceSheet.objects.filter(date = datetime.date.today())
	if transactionToday:
		message = {'date': transactionToday[0].date,
						"incoming":transactionToday[0].incoming,
						'outgoing':transactionToday[0].outgoing,
						'netBalance':transactionToday[0].netBalance,
						}

	if os.path.isfile('activityBackup/backup'+str(datetime.date.today())+'.sts'):
		message['fileBackup'] = "Data are backuped"
	else:
		message['fileBackup'] = 'Data left to be Backuped'
	
	return render_to_response('ioestu/endofday.html', message, RequestContext(request))







def temp(request):
	transactions = balanceSheet.objects.order_by('-date')[0:10]
	transactionData = [item.netBalance for item in transactions]
	transactionDate = [item.date for item in transactions]
	incomingTransaction = [item.incoming for item in transactions]
	outgoingTransactions = [item.outgoing for item in transactions]

	studentid = '067BCT546'
	studentActivity = Activity.objects.filter(student_id=studentid, atype='payment').order_by('-date')[0:10]
	totalExpenses = [item.amount for item in studentActivity]
	expensesDate = [item.date for item in studentActivity]




	return HttpResponse(totalExpenses)



