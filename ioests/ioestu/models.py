from django.db import models, connection
import datetime

class Student(models.Model):
	student_id = models.CharField(max_length=20,primary_key=True)
	firstname = models.CharField(max_length=20)
	lastname = models.CharField(max_length=20)
	lastlogin = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	balance = models.FloatField()
	emailid = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.firstname

class Operator(models.Model):
	name = models.CharField(max_length=20)
	password = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name


class activityCustomQuery(models.Manager):
	def getTodaysActivity(self):
		cursor = connection.cursor()
		cursor.execute('''
				select * from ioestu_activity 
				where date between now()- interval '1 days' + interval '+5:45' HOUR TO MINUTE and now() + interval '+5:45' HOUR TO MINUTE
				''')
		return cursor

class Activity(models.Model):
	student = models.ForeignKey('Student')
	atype = models.CharField(max_length=30)
	operator = models.ForeignKey('Operator')
	details = models.CharField(max_length=50)
	amount = models.FloatField()
	date = models.DateTimeField(default=datetime.datetime.now)
	objects = activityCustomQuery()
	def __unicode__(self):
		return self.atype


