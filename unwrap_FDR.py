import sys,os

for line in sys.stdin:	
	line=line.replace("\n", "")
	data=line.split(" ")
	for i in data:
		print i

