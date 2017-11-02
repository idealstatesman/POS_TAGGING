import nltk
import math


tags = ['DET','N','ADJ','VD','P','PUNCT','CNJ','ADV','WH','V','TO','PRO','NUM','MOD','EX','FW','UH','X']
result = [] 
def sentences():
	print "here"
	corpus = nltk.corpus.brown.tagged_words(simplify_tags=True)
	global simple_corpus 
	simple_corpus = []
	simple_corpus = list(corpus)

	i = -1
	for word in simple_corpus:
		i = i + 1
		temp = []
		temp =  list(word)
		if word[1] == 'NP':
			temp[1] = 'N'
		elif word[1] == 'VN' or word[1] == 'VBZ' or word[1]== 'VG':
			temp[1] = 'V'
		elif word[1] == 'NIL':
			temp[1] = 'X'
		elif word[1] in ['.','?']:
			temp[1] = '<sentence>'
		elif word[1] in [',',';','!',':',')','(','*','``']:
			temp[1] = 'PUNCT'
		elif word[1] in ['VB+PPO', 'VB+IN','VBG+TO','VBN+TO','VB+RP', 'VB+JJ','VB+VB','VB+TO','VB+AT']:
			temp[1] = 'V'
		simple_corpus[i] = tuple(temp)
	'''seen = set()
	ans = []
	for val in simple_corpus :
		if val[1] not in seen:
			ans.append(val)
			seen.add(val[1])'''

	global sentence
	print "give a sentence\n"
	sentence = []
	sentence = (raw_input()).split(" ")
	sentence_length = len(sentence)
	viterbi(len(tags),sentence_length)		



def emission_probabilities(tag_position, word_position):

	word = sentence[word_position]
	tag =  tags[tag_position]
	num_count = 0
	deno_count = 0

	for value in simple_corpus:
		if value[1] == tag:
			deno_count = deno_count + 1
			if value[0] == word:
				num_count = num_count + 1

	if(deno_count>num_count):
		probability =  float(num_count)/ (deno_count)
	else:
		probability = 0.0000001

	if probability == 0:
		probability = 0.0000001
	
	return probability	



def transition_probabilities(prev_tag,tag):
	if tag == len(sentence):
		curr_tag = '<sentence>'
	else:
		curr_tag = tags[tag]
	if prev_tag == -1:
		prev_tag = '<sentence>'
	else:
		prev_tag = tags[prev_tag]
	num_count = 0
	deno_count = 0
	i = -1
	for value in simple_corpus:
		i = i + 1
		if(i<len(simple_corpus)-1):
				if value[1] == prev_tag:
						deno_count = deno_count+1
						if simple_corpus[i+1][1] == curr_tag:
							num_count = num_count + 1
	if(deno_count>num_count):
		probability = float(num_count)/ (deno_count)
	else:
		probability = 0.0000001

	if probability == 0:
		probability = 0.0000001


	return probability	
			




def viterbi(tag_length, sentence_length):
	

	global best
	global backtrack_tag
	best = [[x for x in range(0,sentence_length+1)]for y in range(0,len(tags))]
	backtrack_tag = [[x for x in range(0,sentence_length+1)]for y in range(0,len(tags))]
	for i in range(0,sentence_length+1):
		if(i==0):
			for j in range(0,tag_length):
				best[j][i] =  -math.log10(emission_probabilities(j,i)) -math.log10(transition_probabilities(-1,j))
				backtrack_tag[j][i] = -1;
		elif i==sentence_length: 
			minimum = best[0][i-1]  - math.log10(transition_probabilities(0,i))
			b_tag = 0
			for j in range(1,tag_length):
				inter = - math.log10(transition_probabilities(j,i))
				if inter < minimum:
					minimum = inter
					b_tag = j
					
			best[0][i] = minimum
			backtrack_tag[0][i] = b_tag		
		else:
			for k in range(0,tag_length):
				minimum = best[0][i-1] -math.log10(emission_probabilities(k,i)) - math.log10(transition_probabilities(0,k))
				b_tag = 0
				for j in range(1,tag_length):
					inter = best[j][i-1] - math.log10(emission_probabilities(k,i)) - math.log10(transition_probabilities(j,k))
					if  inter < minimum:
						minimum = inter
						b_tag = j
				best[k][i] = minimum 
				backtrack_tag[k][i] = b_tag	


	index = sentence_length
	jindex = 0

	while(1):
		
		a = backtrack_tag[jindex][index]
		if a == -1:
			break
		b = tags[a]
		result.append(b)
		index = index-1
		jindex = a

	result.reverse()
	print result




	
sentences()


