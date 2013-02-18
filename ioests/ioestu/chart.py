from django import template
from django.http import HttpResponse
from django.shortcuts import render_to_response
from math import sin
from models import *

def render_examples(request):
	data = {
			'data1' : [10, 20, 30],
			'data2' : [i**2 for i in range(20)],
			'data3' : [i**2 for i in range(20, 0, -1)],
			'data4' : [sin(i/5.0)*5 for i in range(100)],
			'venn' : [100, 80, 60, 30, 30, 30, 10],
			'mapdata': {'KS': 0, 'CA': 100, "MN": 50},
			'grid_lines_data': [(6,5), (6,10), (6,15)],
			'grid_lines_style': [('FFFFFF','1','1'), ('FFFFFF','2','1'), ('FFFFFF','3','1'),]
	}
	examples = []
	chart = '''
		{% chart %}
			{% chart-data data1 %}
			{% chart-size "300x200" %}
			{% chart-type "pie" %}
			{% chart-labels "One" "Two" "Three" %}
			{% chart-alt "It worked!" %}
		{% endchart %}
		'''
	t = template.Template("{% load charts %}" + chart)
	rendered = t.render(template.Context(data))
	examples.append({
			'title' : 'this is title',
			'template' : 'line chart',
			'image' : rendered,
		})
	return render_to_response('ioestu/chart.html', {'examples':examples, 'data':data})

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

def getPieChart(data, items):
	data = {'data' : data,
			'items' : items,
			 }
	chart = '''
		{% chart %}
			{% chart-data data %}
			{% chart-size "300x200" %}
			{% chart-type "pie" %}
			{% chart-labels items %}
			{% chart-title "Pie-Chart!" 18 "cc0000" %}
		{% endchart %}
		'''

	t = template.Template("{% load charts %}" + chart)
	rendered = t.render(template.Context(data))
	return rendered

