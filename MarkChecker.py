import requests
import re
url = 'https://ta.yrdsb.ca/yrdsb/index.php'
values = {'username': '',
          'password': ''}
count = 0
search_str = "mark "
courseCode = re.compile("([A-Z][A-Z][A-Z][0-9][A-Z][0-9]-[0-9][0-9])")
marks = {}
newMarks = {}
course = ""
mark = ""
inp1 = ""
inp2 = ""
#r = requests.post(url, data=values)
#response = r.content;

#get curr input DELETE
with open('responseData', 'r') as d : 
	response = d.read()

#GOING TO HAVE TO CHANGE THIS TO READ LAST ENTRY 
with open('History', 'r') as m:
	inp1 = m.readline().rstrip()
	while inp1 or inp2:
		inp2 = m.readline().rstrip()
		d = {inp1: inp2}
		marks.update(d)
		inp1 = m.readline().rstrip()
if '' in marks :
	del marks['']

for i in range(len(response)) : 
	if courseCode.match(response[i : i + 9 ]) :
		course = response[i : i + 9]
		if response.find("Please see teacher for current status regarding achievement in the course", i) > -1 :
			if response.find(search_str, i) < response.find("Please see teacher for current status regarding achievement in the course", i) :
				mark = response[response.find(search_str, i) + 10 : response.find(search_str, i)+13]
			else :	
				mark = 'Mark unavailable'
		else : 
			mark = response[response.find(search_str, i) + 8 : response.find(search_str, i)+13]
	add = {course: mark}
	newMarks.update(add)
del newMarks['']

if marks != newMarks :
	with open('History', 'a') as a:
		a.write("\n")
		for k, v in newMarks.iteritems() :
			a.write(k)
			a.write("\n")
			a.write(v)
			a.write("\n")

#ADD DATE
#checking for a change
#saving to file
#reading from file
#automatic run
