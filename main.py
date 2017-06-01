import urllib.request
from xml.dom import minidom
from bs4 import BeautifulSoup
from xml.etree.ElementTree import parse
import string
from collections import Counter
import datetime as dt
from pymongo import MongoClient

#default url
url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=4661086"
unwanted_chars = ".,()[]"

#setup mongodb
client = MongoClient()
db = client.task1
collection = db.publications
pubData = {}

#get xml and parse it
content = urllib.request.urlopen(url).read()
soup = BeautifulSoup(content, "xml")

#record time
n1 = dt.datetime.now()

#parse the body portion of publication
bodyText = soup.find("body").text
bodyText=bodyText.translate(str.maketrans('','',unwanted_chars))
bodyWords = bodyText.split()
bodyWordFreq = {}
bodyWordFreq = Counter(bodyWords)

figData = {}
i = 1
#parse each figure info for publication
for fig in soup.find_all("fig"):
	figTitle = fig.find("label").text
	print("===============", figTitle, "=================")
	figTitle = "fig"+str(i)
	print(i, figTitle)
	i=i+1

	figData[figTitle]={}
	figText = fig.find("caption").text
	figText2 = figText.translate(str.maketrans('','',unwanted_chars))
	figText3 = figText2.split()
	figTextFreq = Counter(figText3)
	figData[figTitle]["url"] = fig.find("graphic")['xlink:href']
	figData[figTitle]["caption"] = figText
	#print("figure url is: ", fig.find("graphic")['xlink:href'])

	#used to store word co-occurrences
	cooc = {}
	for word in figTextFreq:
		print(word)
		if word in bodyWordFreq:
			print("exist:", figTextFreq[word], bodyWordFreq[word])
			cooc[word] = figTextFreq[word] + bodyWordFreq[word]
		else:
			print("does not exist")
	figData[figTitle]["cooc"] = cooc

pubData["figData"] = figData

print(pubData)

#record end time
n2=dt.datetime.now()
print((n2-n1).microseconds)





