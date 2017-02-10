import requests
from bs4 import BeautifulSoup
import re
import time
start_time = time.time()
#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')
url = 'http://nytimes.com'
result = requests.get(url)
soup = BeautifulSoup(result.text, 'html.parser')

story_heading = soup.find_all('h2', class_ = 'story-heading')
for i in range(10):
	if story_heading[i].a:
		print(story_heading[i].a.text.replace('\n', " ").strip())
	else:
		print(story_heading[i].contents[0].strip())

# #### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

mi_url = 'https://www.michigandaily.com/'
mi_result = requests.get(mi_url)
mi_soup = BeautifulSoup(mi_result.text, 'html.parser')

for div in mi_soup.find_all('div', {'class':"panel-pane pane-mostread"}):
	for li in div.find_all('li'):
		print(li.a.contents[0])

# #### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

marks_url = "http://newmantaylor.com/gallery.html"
marks_result = requests.get(marks_url)
marks_soup = BeautifulSoup(marks_result.text, 'html.parser')

for img in marks_soup.find_all('img'):
	try:
		print(img['alt'])
	except:
		print("No alternative text provided!!")

#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

def getemails(url, chunk):
	count = 1
	umsi_result = requests.get(umsi_url)
	umsi_soup = BeautifulSoup(umsi_result.text, 'html.parser')
	for div in umsi_soup.find_all('div', {'class' : "field-item even"}):
		for a in div.find_all('a', href = True):
			link = a['href']
			new_page = requests.get('https://www.si.umich.edu' + link)
			new_page_soup = BeautifulSoup(new_page.text, 'html.parser')
			for div in new_page_soup.find_all('div', {'class' : "field-item even"}):
				for a1 in div.find_all('a', href= True):
					email = a1['href']
					x = re.findall('mailto:(.+)', email)
					if x != []:
						print(count + chunk, x[0])
						count+=1

chunk = 0
page = 1
umsi_url = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4"			
for each in range(6):
	getemails(umsi_url, chunk)
	umsi_url = umsi_url + '&page=' + str(page)
	chunk = chunk +20
	page +=1

end_time = time.time()
print("total time to process=", str(end_time - start_time), "seconds")