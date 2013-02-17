from django.db import models, connection
import datetime

class Student(models.Model):
	student_id = models.CharField(max_length=50,primary_key=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	lastlogin = models.DateTimeField(default=datetime.datetime.now())
	password = models.CharField(max_length=50)
	balance = models.FloatField()
	emailid = models.CharField(max_length=100, unique=True)

	def __unicode__(self):
		return self.firstname

class Operator(models.Model):
	name = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name


class activityCustomQuery(models.Manager):
	def getTodaysActivity(self):
		cursor = connection.cursor()
		cursor.execute('''
				select * from ioestu_activity where date between current_date and now()
				''')
		return cursor
	def backItUp(self):
		cursor = connection.cursor()
		cursor.execute('''
				select * into ioestu_backupactivity 
				from ioestu_activity 
				where date between now()- interval '1 days' + interval '+5:45' HOUR TO MINUTE and now() + interval '+5:45' HOUR TO MINUTE
			''')
		# cursor.execute("pg_dump -t 'ioestu_backupactivity'")
		return True

class Activity(models.Model):
	student = models.ForeignKey('Student')
	atype = models.CharField(max_length=30)
	operator = models.ForeignKey('Operator')
	details = models.CharField(max_length=50)
	amount = models.FloatField()
	date = models.DateTimeField(default=datetime.datetime.now())
	objects = activityCustomQuery()
	def __unicode__(self):
		return self.atype

class balanceSheet(models.Model):
	incoming = models.FloatField()
	outgoing = models.FloatField()
	date = models.DateField(primary_key = True)
	netBalance = models.FloatField()
	def __unicode__(self):
		return self.netBalance	
