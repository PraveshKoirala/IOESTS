from ioestu.models import Student,Operator, Activity
import re
import hashlib

#get user with password
def getstudentp(username,password):
    try:
        student = Student.objects.get(student_id=username,password=hash(password))
        return  student 
    except Student.DoesNotExist:
        return None
    
#get operator with password
def getoperatorp(username,password):
    try :
        operator = Operator.objects.get(name=username,password=password )
        return operator
    except Operator.DoesNotExist:
        return False

#get student without password
def getstudent(username):
    try:
        student = Student.objects.get(student_id=username)
        return  student 
    except Student.DoesNotExist:
        return None

def getoperator(username):
    try :
        operator = Operator.objects.get(name=username)
        return operator
    except Operator.DoesNotExist:
        return False

        
def usernamevalid(studentid):
    if re.match(r'^\w+',studentid):
        return 'True'
    return r'Student id not matched, the pattern is "[a-bA-B0-9]+"'

def emailvalid(email):
    if re.match(r'^\w+@\S+\.[a-zA-Z]+',email):
        return 'True'
    return r'email not matched, the pattern is "^\w+@\S+\.[a-ZA-Z]+"'

def namevalid(name):
    if re.match(r'^[a-zA-Z]+$',name):
        return 'True'
    return r'name not matched, the pattern is "^[a-zA-Z]+$"'

def verifypassword(password):
    if not password:
        return False
    l = len (password)
    if l <=5:
        return False
    return True

def hash(password):
    l = hashlib.md5(password).hexdigest()
    l = password + l + password
    return hashlib.md5(l).hexdigest()

import random
import string
def getsalt():
    return ''.join(random.choice(string.ascii_letters) for i in range(5))