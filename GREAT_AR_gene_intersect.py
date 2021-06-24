import sys,os

#print len(sys.argv)
GREATfile=open(sys.argv[2])
GREAT=[]
for Gline in GREATfile:
	Gd=Gline.split("\t")
	GREAT.append(Gd[3])

if len(sys.argv)>3:
	new_size=int(sys.argv[3])
	import random
	spotlist=[]
	i=0
	picks=[]
	while i<new_size:
		pick=random.randint(0,len(GREAT)-1)
		if pick in picks:
			pass
		else:
			spotlist.append(GREAT[pick])
			picks.append(pick)
			i+=1
#			print i
	GREAT=spotlist


#print GREAT

file=open(sys.argv[1])

score=0
for line in file:
#	print line[:-1]
	for gene in GREAT:
		if line[:-1]==gene:
			score+=1
print score
