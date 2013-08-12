import requests
from bs4 import BeautifulSoup
import pprint
from tests import tests

def remove_wiki(lst):
	res = []
	for item in lst:
		item = item.lower().strip()
		_id = item.find("wikipedia")
		if _id > -1:
			res.append(item[:_id])
	return res

def search_google(txt):
	res = requests.get("https://www.google.com/search?q="+ txt + " + wikipedia + imdb")
	html_doc = res.text.encode("ascii", errors="ignore")
	soup = BeautifulSoup(html_doc.decode("utf-8"))
	tags = soup.find_all("h3")
	result = []
	for item in tags:
		#if item.get("class") == "r":
			try:
				result.append(item.text)
			except:
				pass

	return result

if __name__ =="__main__":
	for test in tests:
		sr = search_google(test)
		rw = remove_wiki(sr)
		pprint.pprint(rw)