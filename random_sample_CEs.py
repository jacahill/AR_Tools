import sys,os
import random

def load(filename):
	Elements=[]
	file=open(filename)
	for line in file:
		data=line.split("\t")
		Elements.append(data[0]+"-"+data[1]+"-"+data[2])
	return Elements
	
CE=load(sys.argv[1])
ARcount=int(sys.argv[2])
CEcount=len(CE)


SimAR=[]
while len(SimAR)<100:
	pin=random.randint(1,CEcount)-1 ## To switch from base 1 to base 0
	if CE[pin] in SimAR:
		pass
	else:
		SimAR.append(CE[pin])
	
for i in SimAR:
	print i
