# -*- coding: utf-8 -*-
import os,re,sys,math

def CleanEmpty(s) :
	c = s.count('')
	for i in range(0,c) :
		s.remove('')

if len(sys.argv) != 3 :
	print "Usage: " + sys.argv[0] + " [options] <words-txt> <sentence> "
	print "e.g.: " + sys.argv[0] + " model/lang/words.txt \"THIS IS A BOOK\""
	print "options: "
	print "			"
	exit()
	
words_txt = sys.argv[1]
sentence = sys.argv[2]

dict = {}
ifp = open(words_txt,'r')
while True :
	line = ifp.readline()
	if not line: 
		break
	line_list = re.split('\n|\t| ',line)
	CleanEmpty(line_list)
	if line_list[0][0] != '<' and line_list[0][0] != '#' :
		dict[line_list[0]] = int(line_list[1])
ifp.close()

sentence_list = re.split('\n|\t| |#',sentence)
CleanEmpty(sentence_list)
for w in sentence_list :
	if dict.get(w) == None :
		print 'Error Words!'
		exit()
print 'No Error.'






