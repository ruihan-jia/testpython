import urllib.request
from xml.dom import minidom
from bs4 import BeautifulSoup
from xml.etree.ElementTree import parse
import string
from collections import Counter
import datetime as dt
from pymongo import MongoClient


#record time
n1 = dt.datetime.now()

#default url
api = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id="
#pid = "4661086"
#url = api + pid
unwanted_chars = ".,()[]$"

#with open('pmcids') as f:
with open('pmcids8') as f:
#with open('test') as f:
	content = f.readlines()


#setup mongodb
client = MongoClient()
db = client.task1
collection = db.publications
progress = 1


for x in content:
	url = api + x
	if x == '\n':
		continue
	print("--------------publication no.", progress, "----------------")
	print(url)
	print(x)
	progress = progress + 1

	#get xml and parse it
	content = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(content, "xml")

	#parse the body portion of publication
	if not soup.find("body"):
		continue
	bodyText = soup.find("body").text
	bodyText=bodyText.translate(str.maketrans('','',unwanted_chars))
	bodyWords = bodyText.split()
	bodyWordFreq = {}
	bodyWordFreq = Counter(bodyWords)

	pubData = {}
	figData = {}
	i = 1
	#parse each figure info for publication
	for fig in soup.find_all("fig"):
		if fig.find("label"):
			print("===============", fig.find("label").text, "=================")
		figTitle = "fig"+str(i)
		i=i+1

		figData[figTitle]={}

		if fig.find("graphic"):
			if fig.find("graphic").has_attr('xlink:href'):
				figData[figTitle]["url"] = fig.find("graphic")['xlink:href']
			elif fig.find("graphic").has_attr('href'):
				figData[figTitle]["url"] = fig.find("graphic")['href']

		if fig.find("caption"):
			figText = fig.find("caption").text
			figText2 = figText.translate(str.maketrans('','',unwanted_chars))
			figText3 = figText2.split()
			figTextFreq = Counter(figText3)
			#print(fig.find("graphic"))

			figData[figTitle]["caption"] = figText

			#used to store word co-occurrences
			cooc = {}
			for word in figTextFreq:
				#print(word)
				if word in bodyWordFreq:
					#print("exist:", figTextFreq[word], bodyWordFreq[word])
					cooc[word] = figTextFreq[word] + bodyWordFreq[word]
				#else:
					#print("does not exist")

			figData[figTitle]["cooc"] = cooc


	pubData["pid"] = x
	pubData["figData"] = figData

	result = collection.insert_one(pubData)
	print(result)


#record end time
n2=dt.datetime.now()
print((n2-n1).microseconds)





