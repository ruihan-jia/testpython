import urllib.request
from xml.dom import minidom
from bs4 import BeautifulSoup
from xml.etree.ElementTree import parse
import string
from collections import Counter
import datetime as dt

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=4661086"
unwanted_chars = ".,()[]"

content = urllib.request.urlopen(url).read()

#print (content)
soup = BeautifulSoup(content, "xml")

#print (soup)

n1 = dt.datetime.now()

bodyText = soup.find("body").text
bodyText=bodyText.translate(str.maketrans('','',unwanted_chars))
bodyWords = bodyText.split()

#print(bodyWords)

bodyWordFreq = {}

'''
unwanted_chars = ".,()"
for line in bodyWords:
	#print (line)
	word = line.strip(unwanted_chars)
	#print (word)
	if word not in bodyWordFreq:
		bodyWordFreq[word] = 1
	bodyWordFreq[word] += 1
'''

bodyWordFreq = Counter(bodyWords)

#print(bodyWordFreq)


for fig in soup.find_all("fig"):
	print("===============NEW FIGURE=================")
	figText = fig.text
	figText2 = figText.translate(str.maketrans('','',unwanted_chars))
	figText3 = figText2.split()
	figTextFreq = Counter(figText3)

	for word in figTextFreq:
		print(word)
		if word in bodyWordFreq:
			print("exist:", figTextFreq[word], bodyWordFreq[word])
		else:
			print("does not exist")

'''
test = soup.find_all("fig")[0].text

test=test.translate(str.maketrans('','',unwanted_chars))

test2 = test.split()


test3 = Counter(test2)


#print(test3)

for word in test3:
	word = word.strip(unwanted_chars)
	print(word)
	if word in bodyWordFreq:
		print("exist:", test3[word], bodyWordFreq[word])
	else:
		print("does not exist")
'''

n2=dt.datetime.now()

print((n2-n1).microseconds)

#figs = soup.find_all("fig")

#for d in figs:
#	print (d.text)





