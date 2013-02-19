from django import template
from django.http import HttpResponse
from django.shortcuts import render_to_response
from math import sin
from models import *

def getChart(request):
	pieTitle = 'this si pie title'
	pieTemplate = 'pie'
	pieChart = getPieChart([1,2,3],['one', 'two', 'three'], 'this is the title')
	lineTitle = 'this si line title'
	lineTemplate = 'line'
	lineChart = getLineChart([1,2,3,5,3,7,10], [4,5,6], [4,2,5,7],'this is the title')
	message = {
				"pieChart":pieChart,
				'pieTitle':pieTitle,
				'pieTemplate':pieTemplate,
				"lineChart":lineChart,
				'lineTitle':lineTitle,
				'lineTemplate':lineTemplate,
	}
	return render_to_response('ioestu/chart.html',message)

def getLineChart(data1, data2, data3, labels, ylabels, legends):
	data = {'data1' : data1,
			'data2' : data2,
			'data3' : data3,
			'labels' : labels,
			'ylabels' : ylabels,
			'legends' : legends
			 }
	chart = '''
	{% chart %}
	{% chart-type "line" %}
	{% chart-size "500x300" %}
	{% chart-range-marker "v" "E5ECF9" ".75" ".25" %}
	{% chart-colors "CC0000" "00CC00" "0000CC" %}
	{% chart-data data1 data2 data3 %}
	{% chart-legend legends %}
	{% axis "left" %}
		{% axis-labels ylabels %}
		{% endaxis %}
	{% axis "bottom" %}
		{% axis-labels labels %}
	{% endaxis %}
	{% endchart %}
	'''
	t = template.Template("{% load charts %}" + chart)
	rendered = t.render(template.Context(data))
	return rendered

def getSingleChart(data1, labels, ylabels, legends):
	data = {'data1' : data1,
			'labels' : labels,
			'ylabels' : ylabels,
			'legends' : legends
			 }
	chart = '''
	{% chart %}
	{% chart-type "line" %}
	{% chart-size "500x300" %}
	{% chart-range-marker "v" "E5ECF9" ".75" ".25" %}
	{% chart-colors "CC0000" %}
	{% chart-data data1 %}
	{% chart-legend legends %}
	{% axis "left" %}
		{% axis-labels ylabels %}
		{% endaxis %}
	{% axis "bottom" %}
		{% axis-labels labels %}
	{% endaxis %}
	{% endchart %}
	'''
	t = template.Template("{% load charts %}" + chart)
	rendered = t.render(template.Context(data))
	return rendered

def getLineGraphS(studentId):
	studentActivity = Activity.objects.filter(student_id=studentId, atype='payment').order_by('-date')[0:10]
	totalExpenses = [item.amount for item in studentActivity]
	expensesDate = [item.date.date() for item in studentActivity]
	
	if totalExpenses:
		try:
			maximum = int(max(totalExpenses))
		except:
			maximum = 100

		ylabels = [0, maximum/2, maximum]
		image = getSingleChart(totalExpenses, expensesDate, ylabels, ['expenses', ])
		return image
	return False

def getLineGraphO(request=None):
	transactions = balanceSheet.objects.order_by('-date')[0:10]
	transactionData = [item.netBalance for item in transactions]
	transactionDate = [item.date for item in transactions]
	incomingTransactions = [item.incoming for item in transactions]
	outgoingTransactions = [item.outgoing for item in transactions]

	if transactionData+outgoingTransactions+incomingTransactions:
		try:
			maximum = int(max(transactionData+outgoingTransactions+incomingTransactions))
		except:
			maximum = 100

		ylabels = [0, maximum/2, maximum]
		legends = ['NetBalance', 'Deposits', 'Expenses']
		image = getLineChart(transactionData, incomingTransactions, outgoingTransactions, transactionDate, ylabels, legends)

		# pieImage = getPieChart(totalExpenses, expensesDate)

		# return HttpResponse(image)
		return image#, pieImage
	return False
