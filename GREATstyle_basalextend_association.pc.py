### In thier 2013 paper Capra et al used GREAT's basal and extension method for associating noncoding
### accelerated regions with genes.  
### In this method a basal region of 5k upstream and 1k downstream of the Transcription Start Site
### is guarenteed for all genes.  The associated region then extends up to 100kb in each direction
### until it hits another basal region.  A conseqeunce of this is that most accelerated regions are
### associated with exactly two genes.  Still it provides a useful way of associating potential enhancers


### Update August 23, 2018 - Edited GETgene function to allow for gene= to be the last piece of information.


import sys,os,random

geneGFF="/ru-auth/local/home/jcahill/scratch/pubdata/Galga5/GCF_000002315.4_Gallus_gallus-5.0_genomic.gene.pc.gff"
exonGFF="/ru-auth/local/home/jcahill/scratch/pubdata/Galga5/GCF_000002315.4_Gallus_gallus-5.0_genomic.exon.mtrRNA.gff"
Upstream=5000
Downstream=1000
Extend=1000000


def GETbasal(gff):
	#print gff
	file=open(gff)
	out=[]
	for line in file:
	#	print line
		data=line.split("\t")
	#	print data
		geneName=GETgene(data[8])
		strand=data[6]
		chr=data[0]
		if strand=="+":
			start=int(data[3])-Upstream
			if start<1:
				start=1
			end=int(data[3])+Downstream
			TSS=data[3]
		elif strand=="-":
			start=int(data[4])-Downstream
			end=int(data[4])+Upstream
			if end<1:
				end=1
			TSS=data[4]
		gimme=[chr,start,end,geneName,TSS,strand]
		out.append(gimme)
	out.sort()
	return out

def GETextend(base):
	i=0
	out=[]
	while i<len(base)-1:
		working=base[i]
		giveback=[working[0],"null","null",working[3],working[4],working[5]]
		#print "noww", working
		if i==0:
			next=base[i+1]
			giveback[1]=working[1]-Extend
			if working[0]==next[0]:
				if working[2]+Extend<next[1]:
					giveback[2]=working[2]+Extend
				elif working[2]<next[1]:
					giveback[2]=next[1]
		else:
			
			prev=base[i-1]
		#	print "prev", prev
			next=base[i+1]
			if working[0]==prev[0]:
		#		print working[1], prev[2]
				if prev[2]<working[1]-Extend:
					giveback[1]=working[1]-Extend
				elif working[1]>prev[2]:
		#			print working[1], prev[2]
					giveback[1]=prev[2]
			else:
				giveback[1]=working[1]-Extend
					
			if working[0]==next[0]:
				if working[2]+Extend<next[1]:
					giveback[2]=working[2]+Extend
				elif working[2]<next[1]:
					giveback[2]=next[1]
			else:
				giveback[2]=working[2]+Extend
		if giveback[1]=="null":
			giveback[1]=working[1]
		if giveback[2]=="null":
			giveback[2]=working[2]
		out.append(giveback)
		i+=1
	working=base[i]
	prev=base[i-1]
	giveback=[working[0],"null","null",working[3],working[4],working[5]]

	if working[0]==prev[0]:
		if prev[2]<working[1]-Extend:
			giveback[1]=working[1]-Extend
		elif working[1]>prev[2]:
			giveback[1]=prev[2]
	else:
		giveback[1]=working[1]-Extend
	if giveback[1]=="null":
                giveback[1]=working[1]
        if giveback[2]=="null":
        	giveback[2]=working[2]

	out.append(giveback)
	return out

		
def GETgene(stuff):
	intermed=stuff.split("gene=")
	try:
		intermed2=intermed[1].split(";")
		return intermed2[0]
	except IndexError:
		try:
			return intermed[1]
		except IndexError:
			return stuff

def intersect(data,gff,regtype):
	out=[]
	chr=data[0]
	start=int(data[1])
	end=int(data[2])
	for gffdat in gff:
		if chr==gffdat[0]:
			if end>=int(gffdat[3]) and start<=int(gffdat[4]):
				gffdat[2]=regtype
				gene=GETgene(gffdat[8])
				out.append([chr,str(start),str(end),gene,"exon"])
	return out

def load(gff):
	out=[]
	file=open(gff)
	for line in file:
		out.append(line[:-1].split("\t"))
	file.close()
	return out

def unique(listed):
	out=[]
	for i in listed:
		if i in out:
			pass
		else:
			out.append(i)
	for j in out:
		print "\t".join(j)

basal=GETbasal(geneGFF)
#print basal
extend=GETextend(basal)
#print extend
#for i in extend:
#	i[1]=str(i[1])
#	i[2]=str(i[2])
#	print "\t".join(i)
exon=load(exonGFF)


for line in sys.stdin:
	data=line.split("\t")
	start=int(data[1])
	end=int(data[2])
	Inter=intersect(data,exon,"exon") ## Find exons that overlap the region of interest
	#print Inter
	unique(Inter)
	if len(Inter)==0:
		for i in extend:
			if i[0]==data[0]:
				if start<=i[2] and end>=i[1]:
					zult=[data[0],str(start),str(end),i[3],"noncoding"]	
					print "\t".join(zult)




		
