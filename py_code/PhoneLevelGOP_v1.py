# -*- coding: utf-8 -*-
import os,re,sys,math,time

def CleanEmpty(s) :
	c = s.count('')
	for i in range(0,c) :
		s.remove('')
		
def CheckExist(list,str):
	for a in list :
		if a == str :
			return 'true'
	return 'flase'

if len(sys.argv) != 7 :
	print "Usage: " + sys.argv[0] + " [options] <tau> <reject-rate> <phones-file> <transitions-state> <ali-file> <nnet-feats> "
	print "e.g.: " + sys.argv[0] + " -3 0.5 model/lang/phones.txt model/transitions.txt tmp/ali_ tmp/nnposterior_ "
	print "options: "
	print "			"
	exit()
	

tau = float(sys.argv[1])
reject_rate = float(sys.argv[2])
phones_file = sys.argv[3]
transitions_state = sys.argv[4]
ali_file = sys.argv[5]
nnet_feats = sys.argv[6]



#讀取phones.txt檔案
ifp = open(phones_file, 'r')
phones=[]
while True:
	line = ifp.readline()
	if not line:
		break
	line_list = re.split(' |\n',line)
	if line_list[0][0] == '#' or line_list[0] == '<eps>' or line_list[0] == 'SIL' or line_list[0] == 'SPN' or line_list[0] == 'NSN' :
		time.sleep(0.00001) #donothing
	else :
		phones.append(line_list[0])
ifp.close()
#print "phone dictionary have " + str(len(phones)) + " phones."


#讀取轉換每個frame對應到的state與phone所需的查詢表
ifp = open(transitions_state, 'r')
current_phone=''
current_pdf=0
current_state=0
id2phone={}
id2state={}
state_phone2pdf={}

while True:
	line = ifp.readline()
	if not line:
		break
	line_list = re.split(' |\n|\[|\]',line)
	if line_list[0] == 'Transition-state' :
		current_phone = line_list[4]
		current_pdf = int(line_list[10])
		current_state = line_list[7]
		if state_phone2pdf.get(current_state) == None :
			state_phone2pdf[current_state] = {}
		if state_phone2pdf[current_state].get(current_phone) == None :
			state_phone2pdf[current_state][current_phone] = current_pdf
	elif line_list[1] == 'Transition-id' :
		T_id = line_list[3]
		# 建立 id2phone 的 dictionary
		if id2phone.get(T_id) == None :
			id2phone[T_id] = current_phone
		# 建立 id2state 的 dictionary
		if id2state.get(T_id) == None :
			id2state[T_id] = current_state
	else :
		time.sleep(0.000001) #donothing
ifp.close()

#讀取 NN 之後的 posterior
posterior = []
ifp = open(nnet_feats, 'rb')
while True:
	line = ifp.readline()
	if not line:
		break
	line_list = re.split(' |\n|\r|\[|\]',line)
	CleanEmpty(line_list)
	if line_list[0] != 'key' :
		posterior.append([])
		norm = 0.0
		for f in line_list :
			value = math.exp(float(f))
			posterior[len(posterior)-1].append(value)
			norm += value
		for i in range(0,len(posterior[len(posterior)-1])) :
			posterior[len(posterior)-1][i] /= norm
			
ifp.close()

	


#讀取 align 好的檔案
align = []
ifp = open(ali_file, 'rb')
while True:
	line = ifp.readline()
	if not line:
		break
	line_list = re.split(' |\n|\r',line)
	CleanEmpty(line_list)
	for i in line_list :
		if i != 'key' :
			align.append(i)
ifp.close()


# 計算GOP
GOP_score = []
silence = -9999999
for t in range(0,len(align)) :
	if id2phone[align[t]] != 'SIL' and id2phone[align[t]] != 'SPN' and id2phone[align[t]] != 'NSN' :
		current_state = id2state[align[t]]
		current_phone = id2phone[align[t]]
		current_pdf = state_phone2pdf[current_state][current_phone]
		max_value = 0.0
		for p in state_phone2pdf[current_state] :
			if p != current_phone :
				reg_pdf = state_phone2pdf[current_state][p]
				if posterior[t][reg_pdf] > max_value :
					max_value = posterior[t][reg_pdf]
		GOP_score.append(math.log(posterior[t][current_pdf])-math.log(max_value))
	else :
		GOP_score.append(silence)
		
		
last_phone = None
current_phone = None
value = 0.0
count = 0.0
zero_count = 0.0
phone_count = 0.0
msg = ''
for t in range(0,len(align)) :
	if t == 0 :
		last_phone = id2phone[align[t]]
		current_phone = id2phone[align[t]]
	else :
		current_phone = id2phone[align[t]]
	
	if current_phone != last_phone or t == len(align)-1 :
		if last_phone != 'SIL' and last_phone != 'SPN' and last_phone != 'NSN' :
			out = value/count
			out -= tau
			out_symbol = 1
			phone_count += 1
			if out > 0 :
				out_symbol = 1
			else :
				out_symbol = 0
				zero_count += 1
			msg += str(last_phone) + "\t\t" + str(out_symbol) + " (" + str(value/count) + ")\n"
		last_phone = id2phone[align[t]]
		current_phone = id2phone[align[t]]
		value = 0.0
		count = 0.0
	else :
		value += GOP_score[t]
		count += 1
		
		
miss_pronun = float(zero_count/phone_count)
		
if miss_pronun > 1-reject_rate :
	print "reject"
else :
	print msg

