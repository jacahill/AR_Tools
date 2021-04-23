### Cactus outputs multiple potential matches for regions of the maf file where the best match to the reference is unsuffiecently certain.
### This creates major problems for phast which ends up creating chimeras of the two sequences, so we need to remove them.
##
### This script reads through the maf file and anywhere that we see two sequences it prunes the both. 
### In theory you could still get edge cases where your element of interest goes in on one sequence and leaves on another but you could just as easily have a paralogous alignment without it's complimentary orthologous seqeunce and that wouldn't get caught either.


import sys,os

spp=[""]
block=[]
for line in sys.stdin:
	if len(line)==1:
		for i in block:
			data=i.split("\t")
			try:
				sname=data[1].split(".")[0]
			except IndexError:
				sname=""
			if len(data)<2:
				print i.replace("\n", "")
			elif spp.count(sname)<2:
				print i.replace("\n", "")
		spp=[]	
		block=[]
	if line[0]=="s":
		data=line.split("\t")
		sname=data[1].split(".")
		spp.append(sname[0])
	block.append(line)

