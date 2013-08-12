from pattern.search import search
from pattern.en import ngrams
import gsearch

def nlp(bigram, sent):
	entity = []

	for tup in bigram:
		txt = " ".join(tup)
		print txt
		m = search(txt, sent)
		if m:
			entity.append(txt)
		print m

	return entity

if __name__ == "__main__":
	s = "watch simpsons"
	
	bigram = ngrams(s, n=2)
	sres = gsearch.search_google(s)
	cmd = ["last channel", "previous channel","tune to", "turn to", "watch"]
	sres += cmd
	#print sres
	sent = ""
	for item in sres:
		sent += " - " + item

	res = nlp(bigram, sent)
	if len(res) > 0:
		print res
	else:
		onegram = ngrams(s, n=1)
		res = nlp(onegram, sent)
		print res	