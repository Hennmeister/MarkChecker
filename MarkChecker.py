import requests
import re
url = 'https://ta.yrdsb.ca/yrdsb/index.php'
values = {'username': '',
          'password': ''}

r = requests.post(url, data=values)
response = r.content;

count = 0
search_str = "mark "
courseCode = re.compile("([A-Z][A-Z][A-Z][0-9][A-Z][0-9]-[0-9][0-9])")


for i in range(len(r.content)) : 
	if courseCode.match(r.content[i : i + 9 ]) :
		print r.content[i : i + 9]
		if r.content.find("Please see teacher for current status regarding achievement in the course", i) > -1 :
			if r.content.find(search_str, i) < r.content.find("Please see teacher for current status regarding achievement in the course", i) :
				print r.content[r.content.find(search_str, i) : r.content.find(search_str, i)+13]
			else :	
				print "Mark unavailable"
		else : 
				print r.content[r.content.find(search_str, i) : r.content.find(search_str, i)+13]

#checking for a change
#saving to file
#reading from file
#automatic run
