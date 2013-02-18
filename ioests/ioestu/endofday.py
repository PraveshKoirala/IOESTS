from models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime
from emailTemplates import *
from views import index
import json


import hashlib
import random
import string
def forgotPassword(request):
	message = {}
	if request.method == 'POST':
		userid = request.POST.get('userID')
		if userid:
			user = Student.objects.filter(student_id = userid)
			oper = Operator.objects.filter(name = userid)
			if user:
				#generate token
				salt = ''.join(random.choice(string.ascii_letters) for i in range(5))
				token = hashlib.md5(user[0].student_id + user[0].firstname + user[0].password + salt).hexdigest()
				# message['mail'] = getResetMessage(user[0].firstname, user[0].student_id, token,salt)
				sendEmail(resetSubject, getResetMessage(user[0].firstname, user[0].student_id, token, salt), [user[0].emailid,])
				message['mailIsSend'] = True
			elif oper:
				#send mail
				pass
			else:
				message['error'] = "invalid userID"
	return render_to_response('ioestu/forgotPassword.html', message, RequestContext(request))

def forgotPasswordValidator(request, token):
	message = {}
	salt = token[0:5]
	token = token[5:]
	token, userid = token.split('U')
	user = Student.objects.filter(student_id = userid)
	if user:
		if token == hashlib.md5(user[0].student_id + user[0].firstname + user[0].password + salt).hexdigest():
			message['username'] = user[0].firstname
			if request.method =='POST':
				if changePassword(user[0].student_id, request.POST.get('password'), request.POST.get('confirm')):
					message['passwordChanged'] = True
				else:
					message['invalidPassword'] = "Your Passwords does not match."
			return render_to_response("ioestu/resetPassword.html", message, RequestContext(request))
	return HttpResponseRedirect('/')

def changePassword(userid, password, confirm):
	if password != confirm:
		return False
	user = Student.objects.get(student_id = userid)
	user.password = password
	user.lastlogin = datetime.datetime.now()
	user.save()
	return True



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
	return str(jsonData)


def notificationTrigger(request = None):
	targetList = Student.objects.filter(balance__range=(0, 10))
	mailList = []
	for eachStudent in targetList:
		mailList += [eachStudent.emailid]
	return str(sendEmail(subject = rechargeSubject, message = rechargeMessage, mailingList = mailList))


def accountingTask(request = None):		#type of transaction left to be filled
	totalTrans = Activity.objects.getTodaysActivity()
	totalDeposit, totalCredit, output = 0, 0, ''
	for trans in totalTrans:
		if (trans[2] == 'credit deposited'):
			totalDeposit += trans[5]
		elif (trans[2] == 'credit withdrawed'):
			totalCredit += trans[5]
		elif (trans[2] == 'payment'):
			totalCredit += trans[5]
	netDeposit = totalDeposit - totalCredit
	if balanceSheet.objects.all():
		lastEntry = balanceSheet.objects.all().order_by('-date')[0]
		if not(lastEntry.date == datetime.date.today()):
			netDeposit += lastEntry.netBalance
	balance = balanceSheet(incoming = totalDeposit, outgoing = totalCredit, date = datetime.date.today(), netBalance = netDeposit)
	balance.save()
	sendEmail(reportSubject, getReportMessage(totalDeposit, totalCredit), EMAIL_SUPERUSER)
	return str('accounting task')


from django.core.mail import send_mail
# mail is send via ioests.noreply@gmail.com
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


import os.path
########## only admin should be accessible to this routine
def endOfDayEvents(request):
	message = {}
	transactionToday = balanceSheet.objects.filter(date = datetime.date.today())
	if transactionToday:
		message = {'date': transactionToday[0].date,
						"incoming":transactionToday[0].incoming,
						'outgoing':transactionToday[0].outgoing,
						'netBalance':transactionToday[0].netBalance,
						}
	if os.path.isfile('activityBackup/backup'+str(datetime.date.today())+'.sts'):
		message['fileBackup'] = "Data is backuped"
	else:
		message['fileBackup'] = 'Data is not Backuped'
	if request.method == "POST":
		message['message'] = accountingTask() + backupDatabase() + notificationTrigger()
	return render_to_response('ioestu/endofday.html', message, RequestContext(request))
