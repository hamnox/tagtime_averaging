import time
import copy
import requests
import numpy as np

def elementwise_number(num):
	return_value = np.empty_like(num)
	for cnt,x in enumerate(num):
		try:
			if int(num) + 2 == num + 2:	
				return_value[cnt] = True
			else:
				return_value[cnt] = False
		except:
			return_value[cnt] = True
	return return_value
	
while True:
	filename = raw_input("Log File -->")
#	print filename
	try:
		file = open(filename,'r')
		break
	except:
		pass
#time.sleep(5) # this makes it sleep for 5 seconds
log = file.read()
file.close()

# location = 0
loglist = []
temp = log.rsplit("]")
for ping in temp:
	try:
		pingstamp = int(ping[1:11])
	except:
		continue
	# pingday = ping[ping.find('  [')+8:ping.find('  [')+13]
	pingday = time.strftime("%d",time.localtime(pingstamp))
	ping = ping[ping.find(" ")+1:ping.find('  [')].split()
	if ping == []:
		continue
	for tag in ping:
		if tag.isdigit():
			loglist.append([int(pingday),int(tag),int(pingstamp)])
		else:
			continue
			loglist.append([int(pingday),tag,int(pingstamp)])
		# debug print pingday,tag,pingstamp

by_day_array = np.array(loglist)
datapoints = []
# print by_day_array[:,1]
for day in np.arange(np.min(by_day_array[:,0]),np.max(by_day_array[:,0])):
	daystract = np.logical_and(np.equal(by_day_array[:,0],day*np.ones_like(by_day_array[:,0])), elementwise_number(by_day_array[:,0]))
	temp = np.compress(daystract,by_day_array,0)
	if np.count_nonzero(temp) == 0:
		continue
	datapoints.append({"id":time.strftime("%m%d",time.localtime(np.min(temp[:,2]))) + "x" + str(np.count_nonzero(temp[:,2])), "timestamp":np.max(temp[:,2]),"value":np.mean(temp[:,1]),"comment":"STD: " + str(round(np.std(temp[:,1]),3))})
for x in datapoints:
	print x
payload = {"auth_token":"eq4wJw3enxsFU5yptLsx", "datapoints":str(datapoints).replace("'",'"')}
r = requests.post("https://www.beeminder.com/api/v1/users/hamnox/goals/happiness/datapoints/create_all.json",params=payload)

# {x[0]:[0,0] for x in loglist}   depreciated upon deciding to do stuff by averages.
### depreciated section
# for datum in loglist:
	 # temp = []
	 # for tag in datum[1]:
		 # if tag.isdigit():
			 # digitag = int(tag)
		 # else:
		 	 # temp.append(tag)
	 # try:
		 # dictionary[datum[0]] = [dictionary[datum[0]][0]+digitag,int(dictionary[datum[0]][1])+1,dictionary[datum[0]][2] + temp,dictionary[datum[0]][3] + [datum[2]]]
		 # # print dictionary[datum[0]][2]
		 # # print dictionary
	 # except:
		 # dictionary[datum[0]] = [digitag,1,copy.copy(temp),[datum[2]]]
		 # #print datum[0] + "--" + str(dictionary[datum[0]])

# ### depreciated section
# datapoints = []
# from collections import Counter
# count = 0
# for day in dictionary:
	# if dictionary[day][1] != 0:
		# comment = ""
		# temperfi = dict(Counter(dictionary[day][2]))
		# for val in temperfi:
			# comment += val + ":" + str(temperfi[val]) + " "
		# datapoints.append({"id":int(sum(dictionary[day][3])/(dictionary[day][1]/300+1000)),\
			# "timestamp":dictionary[day][3][-1],"value":int(dictionary[day][0])/float(dictionary[day][1]),
			# "comment":comment})
		# count += 1
	# else:
		# continue
# # payload = {"auth_token":"eq4wJw3enxsFU5yptLsx", "datapoints":str(datapoints).replace("'",'"')}
# r = requests.post("https://www.beeminder.com/api/v1/users/hamnox/goals/happiness/datapoints/create_all.json",params=payload)
# print "\n\n"
# print(r.text)

print "done"

#while location <= len(log):
#	temp = log[location:log.find("]",location)+1]
#	location = log.find("]",location)
	
