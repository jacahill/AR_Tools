import sys,os

refspp="Chicken"
spplist=["ZebraFinch","MediumGroundFinch","WhiteThroatedSparrow","CollaredFlycatcher","AmericanCrow","TibetanGroundTit","Bowerbird","BlueCrownedManakin","GoldenCollaredManakin","Rifleman","Kakapo","Kea","ScarletMacaw","Budgerigar","PeregrineFalcon","RedLeggedSerima","DownyWoodpecker","GoldenEagle","CrestedIbis","EmperorPenguin","Killdeer","Hoatzin","AnnasHummingbird","ChimneySwift","ChuckWillsWidow","CommonCuckoo","AmericanFlamingo","RockDove","Chicken","GreaterPrairieChicken","Mallard","Ostrich","WhiteThroatedTinamous"]

def count_logs(pos,dat,spp):
	logs=[]
	for i in dat:
		logs.append(i[1].split(".")[0])
	out=pos
	for s in spp:
		out.append(str(logs.count(s)))
	count=0
	for j in out[3:]:
		if int(j)>1:
			count+=1
	if count>0:
		print "\t".join(out)
		
#	return out
		


data=[]
results=[]
for line in sys.stdin:
	if line[0]=="a":
		if len(data)>0:
			chr=data[0][1].replace(refspp+".", "")
			start=int(data[0][2])+1
			end=str(start+int(data[0][3]))
			start=str(start)
			pos=[chr,start,end]
			count_logs(pos,data,spplist)
			data=[]
	elif line[0]=="s":
		data.append(line.split("\t"))
	else:
		pass

#for j in results:
#	for k in j:
		#if int(k)>1:
		#	print j 

