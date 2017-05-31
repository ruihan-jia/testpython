import urllib.request
from xml.dom import minidom
from bs4 import BeautifulSoup
from xml.etree.ElementTree import parse
import string

url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=4661086"

content = urllib.request.urlopen(url).read()

#print (content)
soup = BeautifulSoup(content, "xml")

#print (soup)

bodyText = soup.find("body").text
#test=test.translate(str.maketrans('','',string.punctuation))
bodyWords = bodyText.split()

#print(test2)

bodyWordFreq = {}
unwanted_chars = ".,()"

for line in bodyWords:
	#print (line)
	word = line.strip(unwanted_chars)
	#print (word)
	if word not in bodyWordFreq:
		bodyWordFreq[word] = 1
	bodyWordFreq[word] += 1

print(bodyWordFreq)
