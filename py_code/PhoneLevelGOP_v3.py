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
phone_sequence = []
phone_posterior = []
phone_id_sequence = []
last_phone = None
current_phone = None
last_state = None
current_state = None
state_sequence = []
for t in range(0,len(align)) :
	if t == 0 :
		last_phone = id2phone[align[t]]
		current_phone = id2phone[align[t]]
		last_state = id2state[align[t]]
		current_state = id2state[align[t]]
		phone_sequence.append(id2phone[align[t]])
		phone_posterior.append([])
		phone_id_sequence.append([])
	else :
		current_phone = id2phone[align[t]]
		current_state = id2state[align[t]]
	state_sequence.append(last_state)

	if current_phone != last_phone or int(current_state) < int(last_state) :
		last_phone = id2phone[align[t]]
		current_phone = id2phone[align[t]]
		current_state = id2state[align[t]]
		phone_sequence.append(id2phone[align[t]])
		phone_posterior.append([])
		phone_id_sequence.append([])
		
	last_state = current_state
		
	phone_posterior[len(phone_posterior)-1].append(posterior[t])
	phone_id_sequence[len(phone_id_sequence)-1].append(align[t])
	
		
	

msg = '發音(phone)\t正確or錯誤\t\t\t\t是否念成?\n'
msg = ''
zero_count = 0.0
phone_count = 0.0
for i in range(0,len(phone_sequence)) :
	canonical_phone = phone_sequence[i]
	if phone_sequence[i] != 'SIL' and phone_sequence[i] != 'SPN' and phone_sequence[i] != 'NSN' :
		max_value = -99999999
		max_phone = ''
		canonical_value = -99999999
		for p in phones :
			value = 0.0
			for t in range(0,len(phone_posterior[i])) :
				current_state = id2state[phone_id_sequence[i][t]]
				current_pdf = state_phone2pdf[current_state][p]
				value += math.log(phone_posterior[i][t][current_pdf])
				#value += phone_posterior[i][t][current_pdf]
			if p != canonical_phone :
				if value > max_value :
					max_value = value
					max_phone = p
			else :
				canonical_value = value
		
		#gop = (canonical_value - max_value) / len(phone_posterior[i])
		gop = (canonical_value) / len(phone_posterior[i])
		gop_tau = gop - tau
		out_symbol = 0
		phone_count += 1
		if gop_tau > 0 :
			out_symbol = 1
		else :
			out_symbol = 0
			zero_count += 1
		
		#msg += str(canonical_phone) + " " + str(out_symbol) + " " + "(" + str(round(gop,4)) + ") "
		msg += str(canonical_phone) + " " + str(round(gop,4)) + " "
		
		'''if out_symbol == 1 :
			msg += str(canonical_phone) + "\t\t" + str(out_symbol) + " (" + str(round(gop,4)) + ")\n"
		else :
			msg += str(canonical_phone) + "\t\t" + str(out_symbol) + " (" + str(round(gop,4)) + ")\t\t\t\t" + str(max_phone) + "\t\t(" + str(round(max_value/len(phone_posterior[i]),4)) + ")\n"
		'''
#miss_pronun = float(zero_count/phone_count)
miss_pronun = 0
if miss_pronun > 1-reject_rate :
	print "reject"
else :
	print msg
		
		
		
		
		
		
