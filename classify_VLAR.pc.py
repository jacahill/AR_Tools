import sys,os
import subprocess
 
#callme="intersectBed -a " + GFF + " -b " + line

bedtools="~/bedtools2-master/bin/intersectBed"
geneGFF="/ru-auth/local/home/jcahill/scratch/pubdata/Galga5/GCF_000002315.4_Gallus_gallus-5.0_genomic.gene.pc.gff"
exonGFF="/ru-auth/local/home/jcahill/scratch/pubdata/Galga5/GCF_000002315.4_Gallus_gallus-5.0_genomic.exon.mtrRNA.gff"

for line in sys.stdin:
	assoc="none"
	genename="none"
	data=line.split("\t")

#	exoninter=intersectGFF(data,exonGFF)
#	geneinter=intersectGFF(data,exonGFF)

	ggff=open(geneGFF)
	for gene in ggff:
		gdat=gene.split("\t")
		if data[0]==gdat[0] and int(data[2])>=int(gdat[3]) and int(data[1])<=int(gdat[4]):
			assoc="intron"
			egff=open(exonGFF)
			gname=gene.split("Name=")
			gnameb=gname[1].split(";")
			genename=gnameb[0]
			for exon in egff:
				edat=exon.split("\t")
				if data[0]==edat[0] and int(data[2])>=int(edat[3]) and int(data[1])<=int(edat[4]): 
					assoc="exon"
					break
			egff.close()
			break
	ggff.close()
	if assoc=="none":
		ggff=open(geneGFF)
		mindist="none"
		side="none"
		for gene in ggff:
			gdat=gene.split("\t")
			if data[0]==gdat[0]:
				if gdat[6]=="+":
					delta_a=abs(int(data[1])-int(gdat[3]))
					delta_b=abs(int(data[2])-int(gdat[3]))
					delta=min([delta_a,delta_b])
					if delta_a<=delta_b:
						direction="up"
					else:
						direction="down"
				elif gdat[6]=="-":
					delta_b=abs(int(data[1])-int(gdat[4]))
                                        delta_a=abs(int(data[2])-int(gdat[4])) 
                                        delta=min([delta_a,delta_b])
					if delta_a<=delta_b:
                                                direction="up"
                                        else:
                                                direction="down" 	
				if mindist=="none" or delta<mindist:
					mindist=delta
					gname=gene.split("Name=")
					gnameb=gname[1].split(";")
					genename=gnameb[0]
					if mindist<=10000 and direction=="up":
						assoc="5p_10k"
					elif mindist<=10000 and direction=="down":
						assoc="3p_10k"
					else:
						assoc="intergenic"	
				
	if assoc=="exon":
		out=assoc+"\t"+genename+"\t.\t"+line[:-1]
		print out
	elif assoc=="intron":
		out=assoc+"\t"+genename+"\t.\t"+line[:-1]
                print out
	elif assoc=="intergenic":
		out=assoc+"\t"+genename+"\t"+str(mindist)+"\t"+line[:-1]
                print out
	else:
		out=assoc+"\t"+genename+"\t.\t"+line[:-1]
                print out

 
#	file=open("tmp.txt", "w")
#	file.write(line)
#	callme=bedtools+" -a " + GFF + " -b tmp.txt"
#	print callme
#	subprocess.call(bedtools, "-a", GFF, "-b", "tmp.txt")
#	file.close()

