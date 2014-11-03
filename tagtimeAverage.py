import time
import copy
import requests
import numpy as np
import glob
		
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
	

# while True:
	# filename = raw_input("Log File -->")
# #	print filename
	# try:
		# file = open(filename,'r')
		# break
	# except:
		# pass

globby = list(glob.glob('*.log'))
log = ""

for filename in globby:
	file = open(filename,'r')
	file = open(filename,'r')
	log += file.read()
	file.close()

# location = 0
loglist = []
log.replace("/n","")
log.replace("/r","")
temp = log.rsplit("]")

for ping in temp:
	try:
		pingstamp = int(ping[0:11])
	except:
		continue
	# pingday = ping[ping.find('  [')+8:ping.find('  [')+13]
	pingday = time.strftime("%j",time.localtime(pingstamp))
	ping = ping[ping.find(" ")+1:ping.find('  [')].split()
	for tag in ping:
		if tag.isdigit():
			loglist.append([int(pingday),int(tag),int(pingstamp)])
		else:
			continue
			loglist.append([int(pingday),tag,int(pingstamp)])
		# debug print pingday,tag,pingstamp

by_day_array = np.array(loglist)
datapoints = []

for day in np.arange(np.min(by_day_array[:,0]),np.max(by_day_array[:,0])+1):
	daystract = np.logical_and(np.equal(by_day_array[:,0],day*np.ones_like(by_day_array[:,0])), elementwise_number(by_day_array[:,0]))
	temp = np.compress(daystract,by_day_array,0)
	if np.count_nonzero(temp) == 0:
		continue
	#array is [0: month-day string, 1: dayofyear, 2: value, 3: 1st IQ, 4: 3rd IQ, 5: totaltags]
	datapoints.append([time.strftime("%m.%d",time.localtime(np.min(temp[:,2]))), time.struct_time(time.localtime(np.min(temp[:,2])))[7],np.mean(temp[:,1]), np.mean(temp[:,1])-np.percentile(temp[:,1],25),np.percentile(temp[:,1],75)-np.mean(temp[:,1]), np.count_nonzero(temp[:,2])])

for data in datapoints:
	pass#	print "%s Average: %s (IQR: %s-%s)" % (data[0], data[2], data[2]-data[3],data[2]+data[4])

import matplotlib.pyplot as plt


datapoints = np.array(datapoints)
xlabels = datapoints[:,0]
# debug print datapoints
datapoints = datapoints.astype(np.float)

plt.figure()

plt.plot(datapoints[:,1], datapoints[:,2], 'b-')
plt.errorbar(datapoints[:,1], datapoints[:,2],yerr=(datapoints[:,3],datapoints[:,4]))
plt.ylim((0,10))
plt.xlim((np.min(datapoints[:,1])-1,np.max(datapoints[:,1])+1))
plt.xticks(datapoints[:,1], xlabels)
plt.show()

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
		 # dictionary[datum[0]] = s[dictionary[datum[0]][0]+digitag,int(dictionary[datum[0]][1])+1,dictionary[datum[0]][2] + temp,dictionary[datum[0]][3] + [datum[2]]]
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

#print "done"

#while location <= len(log):
#	temp = log[location:log.find("]",location)+1]
#	location = log.find("]",location)
	
