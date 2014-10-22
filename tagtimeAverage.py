#import time
import copy
import requests

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

location = 0
loglist = []
temp = log.rsplit("]")
for ping in temp:
	try:
		pingstamp = int(ping[1:11])
	except:
		continue
	pingday = ping[ping.find('  [')+11:ping.find('  [')+13]
	ping = ping[ping.find(" ")+1:ping.find('  [')].split()
	if ping == []:
		continue
	loglist.append([pingday,ping,pingstamp])
dictionary = {}
# {x[0]:[0,0] for x in loglist}   depreciated upon deciding to do stuff by averages.
### depreciated section
for datum in loglist:
	 temp = []
	 for tag in datum[1]:
		 if tag.isdigit():
			 digitag = int(tag)
		 else:
		 	 temp.append(tag)
	 try:
		 dictionary[datum[0]] = [dictionary[datum[0]][0]+digitag,int(dictionary[datum[0]][1])+1,dictionary[datum[0]][2] + temp,dictionary[datum[0]][3] + [datum[2]]]
		 # print dictionary[datum[0]][2]
		 # print dictionary
	 except:
		 dictionary[datum[0]] = [digitag,1,copy.copy(temp),[datum[2]]]
		 #print datum[0] + "--" + str(dictionary[datum[0]])

### depreciated section
datapoints = []
from collections import Counter
count = 0
for day in dictionary:
	if dictionary[day][1] != 0:
		comment = ""
		temperfi = dict(Counter(dictionary[day][2]))
		for val in temperfi:
			comment += val + ":" + str(temperfi[val]) + " "
		datapoints.append({"id":int(sum(dictionary[day][3])/(dictionary[day][1]/300+1000)),\
			"timestamp":dictionary[day][3][-1],"value":int(dictionary[day][0])/float(dictionary[day][1]),\
			"comment":comment})
		count += 1
	else:
		continue
payload = {"auth_token":"eq4wJw3enxsFU5yptLsx", "datapoints":str(datapoints).replace("'",'"')}
r = requests.post("https://www.beeminder.com/api/v1/users/hamnox/goals/happiness/datapoints/create_all.json",params=payload)
# print "\n\n"
# print(r.text)

print "done"

#while location <= len(log):
#	temp = log[location:log.find("]",location)+1]
#	location = log.find("]",location)
	
