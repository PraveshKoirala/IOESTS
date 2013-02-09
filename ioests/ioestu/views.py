from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from ioestu.models import Student,Operator, Activity
from ioestu.models import Activity
import datetime


def index(request):
	#list_by_credit = Student.objects.all().order_by('credit')
	#return render_to_response('ioestu/index.html', {'list_by_credit': list_by_credit})
    state = "Please log in below..."
    username = password = ''
    if request.method == 'POST':        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = str(request.POST.get('user'))

        state = "wrong entry"

        if user == 'operator':
            all_users = Operator.objects.all()

        elif user == 'student':
            all_users = Student.objects.all() 

        for operator in all_users:
            if operator.name == username and operator.password == password:
                if 'data_ioests' in request.session:
			del request.session.get['data_ioests']
                request.session['data_ioests']={'type':'operator','name':username,'balance_before':'null'}
                return  HttpResponseRedirect('/logged/')
        
    return render_to_response('ioestu/index.html',{'state':state, 'username': username},RequestContext(request))

def logged(request):
    last_Activity = ""
    data_ioests=request.session['data_ioests']
    if data_ioests['type']=='operator':
        state = data_ioests['name']+", successfully logged in!"
        operator = data_ioests['name']
        if request.method == 'POST':  
            student = request.POST.get('student')
            type = request.POST.get('type')
            details = request.POST.get('details')
            amount = int(request.POST.get('amount'))
            students = Student.objects.all()
            last_Activity = "student doesn't exist"            
            operat = Operator.objects.get(name=operator)
            for stu in students:
                if stu.student_id == student:  
                    stud = Student.objects.get(student_id=student)
                    data_ioests['balance_before']=stud.balance
                    activ = Activity(
                            student=stud,atype=type,operator=operat,details=details,amount=amount
                        )
                    activ.save()
                    amount *= (type== 'credit deposited') and 1 or -1 
                    stud.balance += amount
                    stud.save()
                   # del request.session['data_ioests']
                    request.session['data_ioests']=data_ioests
                    last_Activity=""

        Activity_latest = Activity.objects.all()
        if Activity_latest:
            Activity_latest = Activity.objects.all().order_by('-date')[0]
        return render_to_response('ioestu/logged.html',{'state':state,'last_Activity':last_Activity,'Activity_latest':Activity_latest,'balance_before':data_ioests['balance_before']},RequestContext(request))


