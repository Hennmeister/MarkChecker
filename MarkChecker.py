import requests
import re
import os
from datetime import date
from Tkinter import *

date = str(date.today())

url = 'https://ta.yrdsb.ca/yrdsb/index.php'
values = {'username': os.environ['TaUser'],
          'password': os.environ['TaPass']}
r = requests.post(url, data=values)
response = r.content;

def FindUpdatedCourses():
	lineCount = 0
	diff = ""
	newMarks = GetNewMarks()
	recentMarks = GetRecentMarks()
	for key in newMarks.keys() : 
		if recentMarks.get(key) != newMarks.get(key) :
			diff += key + "\n"
	return diff

def UpdateWindow(): 
	root = Tk()
	w = Label(root, text="Your marks have changed!")
	w.pack()
	T = Text(root, height=5, width = 40)
	T.pack()
	text = 'The following courses have been updated:' + FindUpdatedCourses()
	T.insert(END, text)
	root.mainloop()

def GetRecentMarks():
	marks = {}
	inp1 = ""
	inp2 = ""
	with open('/Users/henningl/MarkChecker/History', 'r') as f:
		f.seek(-64, 2)
		inp1 = f.readline().rstrip()
		while inp1 or inp2:
			inp2 = f.readline().rstrip()
			d = {inp1: inp2}
			marks.update(d)
			inp1 = f.readline().rstrip()
	if '' in marks :
		del marks['']
	return marks

def GetNewMarks():
	newMarks = {}
	search_str = "mark "
	course = ""
	mark = 0
	courseCode = re.compile("([A-Z][A-Z][A-Z][0-9][A-Z][0-9]-[0-9][0-9])")

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
	return newMarks

def main():
	newMarks = GetNewMarks()
	if GetRecentMarks() != newMarks :
		with open('/Users/henningl/MarkChecker/History', 'a') as a:
			a.write("\n")
			a.write(date)
			a.write("\n")
			for k, v in newMarks.iteritems() :
				a.write(k)
				a.write("\n")
				a.write(v)
				a.write("\n")
		UpdateWindow()


if __name__ == '__main__':
	main()