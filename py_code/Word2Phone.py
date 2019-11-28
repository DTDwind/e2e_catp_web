# -*- coding: utf-8 -*-
import os,re,sys,math

def CleanEmpty(s) :
	c = s.count('')
	for i in range(0,c) :
		s.remove('')
		
def FindUtteranceMatchPath(utterance_word_sequence, current_phone_sequence, lexicon) :
	word_index_count_sequence = []
	word_index_sequence_dict = {}
	for i in range(0,len(utterance_word_sequence)) :
		word = utterance_word_sequence[i]
		word_index_count_sequence.append(len(lexicon[word]))
	make_sequence2dict(word_index_sequence_dict,word_index_count_sequence,[],0)
	for i in word_index_sequence_dict :
		word_index_sequence = word_index_sequence_dict[i]
		phone_sequence = []
		for j in range(0,len(word_index_sequence)) :
			word_index = word_index_sequence[j]
			word = utterance_word_sequence[j]
			for k in range(0,len(lexicon[word][word_index])) : 
				phone_sequence.append(lexicon[word][word_index][k])
		if current_phone_sequence == phone_sequence :
			return word_index_sequence_dict[i]
	return None
		
def make_sequence2dict(dict,num_sequence,cs,index) :
	ns = []
	if len(dict) < 1000000000000000000000 :
		for i in range(0,len(cs)) :
			ns.append(cs[i])
		if index < len(num_sequence) :
			num = num_sequence[index]
			for i in range(0,num) :
				ns.append(i)
				make_sequence2dict(dict,num_sequence,ns,index+1)
				ns.pop()
		else :
			dict[str(ns)] = ns

if len(sys.argv) != 4 :
	print "Usage: " + sys.argv[0] + " [options] <lexicon-txt> <sentence> <phone-sequence> "
	print "e.g.: " + sys.argv[0] + " data/lexicon.txt \"CLOG\" \"K 1 L 0 AA1 1 G 0\""
	print "options: "
	print "			"
	exit()
	
lexicon_txt = sys.argv[1]
sentence = sys.argv[2]
phone_sequence = sys.argv[3]

lexicon_dict = {}
ifp = open(lexicon_txt,'r')
while True :
	line = ifp.readline()
	if not line: 
		break
	line_list = re.split('\n|\r|\t| ',line)
	CleanEmpty(line_list)
	if line_list[0] != '<SIL>' :
		if lexicon_dict.get(line_list[0]) == None :
			lexicon_dict[line_list[0]] = []
		lexicon_dict[line_list[0]].append(line_list[1:len(line_list)])
ifp.close()

'''for l in lexicon_dict :
	for i in range(0,len(lexicon_dict[l])-1) :
		if lexicon_dict[l][i][0] != lexicon_dict[l][i+1][0] :
			print lexicon_dict[l][i]
			print lexicon_dict[l][i+1]
			print "pig"
			exit()'''

sentence_list = re.split('\n|\r|\t| ',sentence.upper())
sentence_list_low = re.split('\n|\r|\t| ',sentence)
CleanEmpty(sentence_list)
CleanEmpty(sentence_list_low)
phone_sequence_list = re.split('\n|\r|\t| ',phone_sequence)
CleanEmpty(phone_sequence_list)
phone_sequence_without_detection = []
for i in range(0,len(phone_sequence_list)) :
	if i % 2 == 0 : 
		phone_sequence_without_detection.append(phone_sequence_list[i])
		
'''if len(sentence_list) == 1 :
	msg = sentence_list[0] + " 0 " + str(len(phone_sequence_without_detection) * 2)
	print msg'''

msg = ''
index = 1
match_path = FindUtteranceMatchPath(sentence_list,phone_sequence_without_detection,lexicon_dict)
for i in range(0,len(match_path)) :
	word = sentence_list_low[i]
	msg += word + ","
	word_index = match_path[i]
	phone_sequence_len = len(lexicon_dict[word.upper()][word_index])
	for j in range(0,phone_sequence_len) :
		msg += lexicon_dict[word.upper()][word_index][j] + " " + phone_sequence_list[index] + " "
		index += 2
	msg += '\n'
	#msg += word + ' ' + str(index * 2)
	#msg += str((index+phone_sequence_len-1)*2) + '\n'
	#index += phone_sequence_len
print msg,
	