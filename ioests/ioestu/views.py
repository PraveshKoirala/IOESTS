from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from ioestu.models import Student,Operator, Activity
from ioestu.validation import getstudentp, getoperatorp, getoperator,getstudent
import ioestu.validation as validation
from datetime import datetime
from validation import hash


def index(request):
	#list_by_credit = Student.objects.all().order_by('credit')
	#return render_to_response('ioestu/index.html', {'list_by_credit': list_by_credit})
    state = "Please log in below..."
    username = password = ''
    if request.method == 'POST':     
        state = "invalid user id or password"
        username = request.POST.get('username')
        password = request.POST.get('password')
        if getoperatorp(username,password):
            request.session['data_ioests']={'type':'operator','name':username,'balance_before':'null','action':'payment'}
            return  HttpResponseRedirect('/logged/') 
        elif getstudentp(username, password):
            request.session['data_ioests']={'type':'student','name':username,'balance_before':'null','action':'payment'}
            return  HttpResponseRedirect('/logged/') 
        else:
            student = None
            operator = None
    return render(request,'ioestu/index.html',{'state':state, 'username': username})


def logged(request):
    if not 'data_ioests' in request.session:
        return HttpResponseRedirect('/')

    Activity_latest = Activity.objects.all()
    data_ioests=request.session['data_ioests']
    data_ioests['balance_before'] = 'null'
    error = ''
    state = ''
    errordict ={}
    to_month={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
    log = ""
    if data_ioests['type']=='operator':
        log = data_ioests['name']+", successfully logged in!"
        operator = data_ioests['name']
        
        if request.method == 'POST':  
            activity_type = request.POST.get('activity_type')
            if activity_type == 'create_account':
            	error = addaccount(request)
            	if error == True: #if the account was created successfully
            		state = "New user %s %s added successfully"%(request.POST['fname'],request.POST['lname'])	
                else:
                    #there is error
                    errordict['student_id'] = request.POST.get('student_id')
                    errordict['fname'] = request.POST.get('fname')
                    errordict['lname'] = request.POST.get('lname')
                    errordict['email'] = request.POST.get('email')
                    
                    
            elif activity_type == 'delete_account':
            	error = delaccount(request)
                if error == True:
                    state = "User %s removed successfully"%(request.POST['student_id'])
            elif activity_type == 'deposit':
                error = deposit(request)
                if error == True:
                    state = "%s deposited in %s account"%(request.POST['amount'],request.POST['student_id'])
                else: 
                    errordict['student_id']=request.POST.get('student_id')
                    errordict['amount']=request.POST.get('amount')
                    
            elif activity_type == 'payment':
                error = payment(request)
                if error == True:
                    Activity_latest = Activity.objects.all()
                    if Activity_latest:
                        Activity_latest = Activity.objects.all().order_by('-date')[0]
                	state = 'A payment of %s made by %s'%(request.POST['amount'],request.POST['student_id'])
                else:
                	errordict['student_id']=request.POST.get('student_id')
                	errordict['amount']=request.POST.get('amount')
                	errordict['details']=request.POST.get('details')
            
		
            else:
            	#TODO: write code for other actions
            	pass
            
        
        if error == True:
            error = None
            
        context = {'state':state,'error':error, 'balance_before':data_ioests['balance_before'],'Activity_latest':Activity_latest,'log':log}
        
        
        if len(errordict): #if error dictionary is not empty, update the context
            context.update(errordict)
    
        
        #in case we have to modify the response header.
        response = render(request,'ioestu/logged_operator.html',context)
        
        return response
    
    else:
        state = ''
        student = Student.objects.get(student_id=data_ioests['name'])
        activities = Activity.objects.filter(student_id=student.student_id).order_by('-date')
        dateset = []
        for d in activities:
            date = str(to_month[d.date.month])+', '+str(d.date.year)
            if date not in dateset:
                dateset.append(date)

        log = data_ioests['name']+", successfully logged in!"
        if request.method == "POST":
            activity_type = request.POST.get('activity_type')
        	
            if activity_type == "changedetails":
        		if request.POST.get('newpassword'):
        		 	error = changepassword(request)
        		  	if error == True:	#if successful
        			   state = "Password changed successfully"
        			
        			
        		elif request.POST.get('newemail'):
        			error = changeemail(request)
        			if error == True:
        				state = "Email changed successfully"
        			else:
        				errordict['newemail'] = request.POST.get('newemail')
            else:
                search_time = request.POST.get('date')
                keyword = request.POST.get('keyword')
                if search_time:
                    if not search_time == "all" and not keyword == '':
                        year = search_time[-4:]
                        month = to_month.keys()[to_month.values().index(search_time[:3])]
                        activities = Activity.objects.filter(date__year = year, date__month = month,details__regex=r'(.*%s.*)'%keyword).order_by('-date')
                    elif not search_time == "all":
                        year = search_time[-4:]
                        month = to_month.keys()[to_month.values().index(search_time[:3])]
                        activities = Activity.objects.filter(date__year = year, date__month = month).order_by('-date')
                    elif not keyword == '':
                        activities = Activity.objects.filter(details__regex=r'(.*%s.*)'%keyword).order_by('-date')

        	
        else:
            pass
        
        #return render_to_response('ioestu/logged_student.html',{'state':state,'student':student,'activities':activities})
        if error == True:
        	error = ''
        context = {'state':state,'error':error, 'balance_before':data_ioests['balance_before'],'student':student,'activities':activities,'log':log,'dateset':dateset}
        if len(errordict):
        	context.update(errordict)
        return render(request,'ioestu/logged_student.html',context)


def payment(request):
    sid = request.POST.get('student_id')
    password = request.POST.get('password')
    opname = request.session['data_ioests'].get('name')

    student = getstudentp(sid,password)
    operator = getoperator(opname)
    details = request.POST.get('details')

    if not(student and operator):
    	return "Student or Operator doesn't exist"

    amount = request.POST.get('amount')
    if not amount:
    	return 'Amount field can\'t be empty'

    try:
    	amount = float(amount)
    except:
    	return "Invalid Balance. Must be a float number"

    if amount >1000:
    	return "Can't pay more than Rs 1000 at a time"

    if amount > student.balance:
       return "Insufficient funds"

    data_ioests = request.session['data_ioests']
    data_ioests['balance_before']=student.balance
    request.session['data_ioests']=data_ioests
    student.balance -= amount
    activ = Activity(student=student,atype='payment',operator=operator,details=details,amount=amount)
    activ.save()

    student.save()

    #TODO: create activity
    return True


def deposit(request):
    sid = request.POST.get('student_id')
    password = request.POST.get('password')
    oppassword = request.POST.get('operatorpassword')
    student = getstudentp(sid,password)
    operator = getoperatorp(request.session['data_ioests'].get('name'),oppassword)
    details = request.POST.get('details','amount deposited')
    if not (student and operator):
        return "Student or Operator doesn't exist"
    
    amount = request.POST.get('amount')
    if amount == None:
        return "Amount field can't be empty"
    try:
        amount = float(amount)
    except:
        return "Invalid Balance. Must be a float number"
    
    if amount >1000:
        return "Can't deposit more than Rs 1000 at a time"
    
    student.balance += amount
    student.save()
    activ = Activity(student=student,atype='deposit',operator=operator,details=details,amount=amount)
    activ.save()
    student.save()
    #TODO: create activity
    return True


def addaccount(request):
	#check if another operator and student has this name
	uname = request.POST.get('student_id')
	if getoperator(uname) or getstudent(uname):
		return 'The id already exists'
	password = validation.hash(uname)
	email = request.POST.get('email')
	firstname = request.POST.get('fname')
	lastname = request.POST.get('lname')
	
	operator = getoperator(request.session['data_ioests'].get('name'))
	if not operator:
		return "Operator doesn't exist. Please Log in first "
	details = request.POST.get('details','new account created')
	
	#validate these credentials
	error = validation.usernamevalid(uname)
	if error != 'True': return error
	error = validation.emailvalid(email)
	if error != 'True': return error
	error = validation.namevalid(firstname)
	if error != 'True': return error
	error = validation.namevalid(lastname)
	if error != 'True': return error
	
	s = Student(student_id=uname,firstname=firstname,lastname=lastname,password=password,balance=100.,emailid=email,lastlogin=datetime.now())
	s.save()
	activ = Activity(student=s,atype='newaccount',operator=operator,details=details,amount=100.)
	activ.save()

	return True

def delaccount(request):
	s = getstudentp(request.POST.get('student_id'),request.POST.get('password'))
	if not s:
		return 'The id doesn\'t  exists'
	s.delete()
	return True




def changepassword(request):
	sid = request.session['data_ioests'].get('name')
	password = request.POST.get('oldpassword')
	newpassword = request.POST.get('newpassword')
	student = getstudentp(sid,password)
	if not student:
		return 'Authentication error. '
	if not validation.verifypassword(newpassword):
		return 'Password invalid. Must be more than 5 characters'
	student.password = validation.hash(newpassword)
	student.save()
	return True
		
	
	
def changeemail(request):
	sid = request.session['data_ioests'].get('name')
	password = request.POST.get('oldpassword')
	newemail = request.POST.get('newemail')
	student = getstudentp(sid,password)
	if not student:
		return 'Authentication error. '
	error = validation.emailvalid(newemail)
	if error != 'True':
		return error
	student.email = newemail
	student.save()
	return True

from emailTemplates import *
from validation import getsalt
import hashlib
from validation import hash
def forgotPassword(request):
    message = {}

    if request.method == 'POST':
        userid = request.POST.get('userID')
        if userid:
            user = Student.objects.filter(student_id = userid)
            oper = Operator.objects.filter(name = userid)
            if user:
                salt = getsalt()
                stringFeed = user[0].student_id + user[0].firstname + user[0].password + salt
                token = hashlib.md5(stringFeed).hexdigest()
                
                mailMessage = getResetMessage(user[0].firstname, user[0].student_id, token, salt);
                sendEmail(resetSubject, mailMessage, [user[0].emailid,])
                message['mailIsSend'] = True
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
        stringFeed = user[0].student_id + user[0].firstname + user[0].password + salt
        if token == hashlib.md5(stringFeed).hexdigest():
            message['username'] = user[0].firstname
            if request.method =='POST':
                password = request.POST.get('password')
                confirm = request.POST.get('confirm')
                if changePassword(user[0].student_id, password, confirm):
                    message['passwordChanged'] = True
                else:
                    message['invalidPassword'] = "Your Passwords do not match."
            return render_to_response("ioestu/resetPassword.html", message, RequestContext(request))
    
    return HttpResponseRedirect('/')

def changePassword(userid, password, confirm):
    if password != confirm:
        return False
    
    user = Student.objects.get(student_id = userid)
    user.password = hash(password)
    import datetime
    user.lastlogin = datetime.datetime.now()
    user.save()
    
    return True

from django.http import HttpResponse
def clearSession(request):
    # session = request.session['data_ioests']
    # if request.session['data_ioests']:
    #     del request.session["data_ioests"]
    if 'data_ioests' in request.session:
        del request.session['data_ioests']
    else:
        data = False
    return HttpResponseRedirect('/')
