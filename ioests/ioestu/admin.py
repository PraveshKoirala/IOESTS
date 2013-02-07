from ioestu.models import Student
from ioestu.models import Activity
from ioestu.models import Operator
from django.contrib import admin

class ActivityInline(admin.TabularInline):
	model = Activity
	extra = 0

class StudentAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,	{'fields':['student_id']}),
		('firstname',	{'fields':['firstname']}),
		('lastname', {'fields':['lastname']}),
		('password',	{'fields':['password'],'classes':['collapse']}),
		(None,	{'fields':['balance']}),
	]
	inlines = [ActivityInline]
	list_display = ('barcode', 'name', 'password','credit')

class OperatorAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,{'fields':['name']}),
		(None,{'fields':['password']}),
	]
	list_display = ('name', 'password')

admin.site.register(Student,StudentAdmin)
admin.site.register(Operator,OperatorAdmin)