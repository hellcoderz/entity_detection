import redis
from tests import tests

class EntityDetection:
  def __init__(self):
    try:
      self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
    except:
      print "Cannot connect to redis"
      exit()

  def ngrams(self, sent, nlen):
  	grams = []
  	words = sent.split()

  	for i in range(len(words)-nlen+1):
  		grams.append(words[i:i+nlen])
  	if len(grams) > 0:
  		return grams
  	else:
		return words

  def all_grams(self, sent):
  	nlen = len(sent.split())
  	result = []
  	for i in range(nlen, 0, -1):
  		#print sent, i
  		result += self.ngrams(sent, i)
  	return result

  def flush(self):
    self.r.flushdb()
  
  def dbsize():
    self.r.dbsize
  
  def load_source(self, path):
    f = open(path, "r")
    count = 0
    for line in f:
      count += 1
      print count 
      try:
        line = line.strip().lower().encode("ascii", errors="ignore")
      except:
        continue
      grams = self.all_grams(line)
      for gram in grams:
        self.r.incr("|".join(gram))

  def join_all(self,grams):
  	jres = []
  	for gram in grams:
  		jres.append(" ".join(gram))
  	return jres

  def known(self, word):
  	return self.r.exists(word)

  def detect_entity(self, sent):
  	sent = sent.lower()
  	grams = self.all_grams(sent)
  	result = []
  	skip = []

	for gram in grams:
		
		if " ".join(gram) in skip:
			skip.append(" ".join(gram[1:]))
			skip.append(" ".join(gram[:-1]))
			continue
		if self.known("|".join(gram)):
			#print " ".join(gram[:-1])
			skip.append(" ".join(gram[1:]))
			skip.append(" ".join(gram[:-1]))
			result.append(" ".join(gram))
	#print skip
	return result  

if __name__ == "__main__":
  red = EntityDetection()
  #red.flush()
  #red.load_source("entity.txt")
  #print "indexing done"
  for test in tests:
  	print test
  	print red.detect_entity(test)
  #print red.all_grams("watch harry potter")