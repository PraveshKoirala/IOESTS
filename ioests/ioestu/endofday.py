from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from emailTemplates import *
import json
import os.path
from ioests.settings import SITE_ROOT

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
	fileName = SITE_ROOT+'/activityBackup/backup'+str(datetime.date.today())+'.sts'
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
		elif (trans[2] == 'newaccount'):
			totalDeposit += 100
	netDeposit = totalDeposit - totalCredit
	
	if balanceSheet.objects.all():
		lastEntry = balanceSheet.objects.all().order_by('-date')[0]
		slEntry = balanceSheet.objects.all().order_by('-date')[1]
		if lastEntry.date != datetime.date.today():
			netDeposit += lastEntry.netBalance
		else:
			netDeposit += slEntry.netBalance
	
	balance = balanceSheet(
		incoming = totalDeposit,
		 outgoing = totalCredit, 
		 date = datetime.date.today(), 
		 netBalance = netDeposit)
	balance.save()
	
	#####sendEmail(reportSubject, getReportMessage(totalDeposit, totalCredit), EMAIL_SUPERUSER)
	
	return True


########## only admin should be accessible to this routine
from chart import *
def endOfDayEvents(request):
	message = {}
	
	if not 'data_ioests' in request.session:
		return HttpResponseRedirect('/')
	if not request.session['data_ioests']['type'] == 'operator':
		return HttpResponseRedirect('/')

	if request.method == "POST":
		accountingTask()
		backupDatabase()
		###notificationTrigger()


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
	
	line = getLineGraphO()
	message['line'] = line

	return render_to_response('ioestu/endofday.html', message, RequestContext(request))



###DATABASE GENERATION CODE
from validation import hash
from validation import getstudent
from validation import getoperator
import random
def sandbox(request):
	a = file("e:/college/lms_member.csv", 'r') 
	item = a.readline()
	datime = datetime.datetime.now()
	while (item):
		container = item.split();
		stuid = container[len(container)-1]
		lastname = container[len(container)-2]
		
		firstname = ""
		for i in xrange(len(container)-2):
			firstname += container[i] + " "
		
		balance = 100
		emailid = container[0] +stuid+'@ioests.ioe.edu.np'
		
		stuData = Student(student_id = stuid, firstname = firstname, lastname = lastname,
							lastlogin = datime, password = hash(stuid), balance = balance, emailid =emailid )
		stuData.save()

		opeData = getoperator("hari")

		actData = Activity(student=stuData,atype='newaccount',operator=opeData,details='new account created',amount=100.)
		actData.save()
		
		item = a.readline()
	return HttpResponse("sandbox test")

def generateActivity(request):
	oNames = ['hari', 'gopal', 'ram', 'gita', 'rita', 'shyam', 'mina']
	for i in xrange(200):
		a = file("E:/College/lms_member.csv", 'r')
		ran = random.choice([j+1 for j in xrange(1930)])
		for j in xrange(ran):
			item = a.readline()
		container = item.split();
		stuid = container[len(container)-1]
		student = getstudent(stuid)
		operator = getoperator(oNames[random.choice([j for j in xrange(len(oNames))])])

		amount = random.choice([j for j in xrange(20)]) + 10

		if amount > student.balance:
			continue

		student.balance -= amount
		activ = Activity(student=student,atype='payment',operator=operator,
								details="For photocopy" if i%2 == 0 else "Canteen expense",amount=amount)
		activ.save()

		student.save()

		a.close()
	return HttpResponse("activities set")
def activityDeposit(request):
	oNames = ['hari', 'gopal', 'ram', 'gita', 'rita', 'shyam', 'mina']
	for i in xrange(50):
		a = file("E:/College/lms_member.csv", 'r')
		ran = random.choice([j+1 for j in xrange(1930)])
		for j in xrange(ran):
			item = a.readline()
		container = item.split();
		stuid = container[len(container)-1]
		student = getstudent(stuid)
		operator = getoperator(oNames[random.choice([j for j in xrange(len(oNames))])])

		amount = random.choice([j for j in xrange(50)]) + 10

		student.balance += amount
		activ = Activity(student=student,atype='deposit',operator=operator,
								details="amount deposited",amount=amount)
		activ.save()

		student.save()

		a.close()
	return HttpResponse("deposit done")
