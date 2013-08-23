import re
import requests
import json
import util
from distance import jarow

prefix_url = ""
suffix_url = "" 
suffix_url1 = ""

def get(txt):
	global prefix_url
	global suffix_url
	global suffix_url1

	entity_type = " AND (entitytype:person)"

	res = requests.get(prefix_url + txt.strip().lower() + suffix_url +suffix_url1)
	return res.text

def get_merlinId(JSON):
	pass

def get_title(JSON):
	title = []
	if JSON["returned"] > 0:
		entities = JSON["entities"]
		for entity in entities:
			title.append(util.normalize(entity["title"][0]["default"]))
		return title
	else:
		return None

def gen_index(lst):
	index = {}
	for item in lst:
		words = util.normalize(item).split()
		for i in range(len(words)):
			if i == 0 and len(words) > 1:
				try:
					index[words[i]]["right"].append(words[i+1])
				except:
					index[words[i]] = {"left":[], "right":[words[i+1]]}
			elif i == len(words)-1 and len(words) > 1:
				try:
					index[words[i]]["left"].append(words[i-1])
				except:
					index[words[i]] = {"right":[], "left":[words[i-1]]}
			else:
				if len(words) > 1:
					try:
						index[words[i]]["right"].append(words[i+1])
						index[words[i]]["left"].append(words[i-1])
					except:
						index[words[i]] = {"left":[words[i-1]], "right":[words[i+1]]}
				else:
					pass
		#print words
	return index

def ngram(txt, n=2):
	words = txt.split()
	wlen = len(words)
	ngrams = []
	if wlen > n:
		for i in range(wlen-n+1):
			ngrams.append(" ".join(words[i:i+n]))
	return ngrams

def gen_ngrams(lst):
	ngrams = []
	for item in lst:
		ngrams += ngram(item)
	return ngrams

def split_and_add(lst):
	arr = []
	rlst = [" and "]
	for item in lst:
		for r in rlst:
			if item.find(r) > -1:
				sp = item.split(r)
				arr += sp
	return arr

def find_similar(sent, lst):
	dist = {}
	lst = lst + split_and_add(lst)
	for item in lst:
		item = util.normalize(item)
		sent = util.normalize(sent)
		d = jarow(item, sent)
		#print item , d
		if d > 0.75:
			dist[item] = d
	#print dist
	max_arr = util.get_max(dist)
	return max_arr

def correct_left(rc, lc, index, rrc=None):
	rc = util.normalize(rc)
	dist = {}
	try:
		left_ctx = index[rc]["left"]
		for item in left_ctx:
			d = jarow(item, lc)
			#print item , (d * 1.0)/len(item)
			#print d
			if d > 0.75:
				dist[item] = d
		max_arr = util.get_max(dist)
		#print dist
		return max_arr
	except:
		return None

def correct_right(lc, rc, index, llc=None):
	lc = util.normalize(rc)
	dist = {}
	try:
		right_ctx = index[rc]["right"]
		for item in right_ctx:
			d = jarow(item, rc)
			#print item , (d * 1.0)/len(item)
			if d > 0.75:
				dist[item] = d
		max_arr = util.get_max(dist)
		#print dist
		return max_arr
	except:
		return None

def long_substr(data):
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and all(data[0][i:i+j] in x for x in data):
                    substr = data[0][i:i+j]
    return substr

def auto_correct(sent):
	#erica badu does not work , should check for it
	#sent = "ericka badu"
	txt = get(sent)
	JSON = json.loads(txt)
	res = get_title(JSON)
	#print res
	if not res == None:
		"""
		index = gen_index(res)
		ans = correct_left("order", "lawn", index)
		if ans == []:
			print find_similar(sent, res)
		"""
		
		return find_similar(sent, res)
	else:
		return "-"

if __name__ == "__main__":
	print auto_correct("erika badu")
	
	
	

