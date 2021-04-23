#Carolyn Khoury 7/17/2017
#Make the data in the "fastas" directory into a useable form by having all lines of genetic data for each species be read as one. Then, using a loop, compare every sequence entry in the alignment with each other. For each sequence entry then divide the number of differences by the number of observable sites, and the number of observable sites by the number of total sites as a quality check. Afterwards, conduct summary statistics on the resulting "usableData" list by finding the mean, median, and standard deviation of the data, and print the 10th-90th percentiles of the data. Then, go back and make it so that the program is doing this whole analysis for chunks of each code (1,000 base pairs long), and make sure to add start and end location of the chunk in the final print of the summary statistics. Now I would like the summary statistics to be redirected into an organized statistics file. 

import sys,os
file=open(sys.argv[1])
species=[]
basePairs=[]
for line in file:
	if(">" in line):
        	species.append(line)
                basePairs.append("")
        else:
                basePairs[-1]+=line[:-1]
def compare(seq1, seq2):
	count=0
        observableSites=0
        differences=0
        sequence1List=[seq1]
        sequence2List=[seq2]
        paralogData1=[]
	nucleotideString="ATCG"
        while(count<len(seq1)):
        	if(seq1[count] in nucleotideString and seq2[count] in nucleotideString):
			observableSites+=1
                	if(seq1[count]!=seq2[count]):
                        	differences+=1
                count+=1
        try:
		divisionDO=float(differences)/float(observableSites)
        except ZeroDivisionError:
		divisionDO="null"
	divisionOL=float(observableSites)/float(1000)
        if(divisionOL>0.1):
        	return divisionDO
       	else:
        	return "null"
sample1Counter=0
sample2Counter=1
usableData=[]
sampleStart=0
sampleEnd=1000
while(sampleEnd<len(basePairs[0])):
	while(sample2Counter<33):
		divDO=compare(basePairs[sample1Counter][sampleStart:sampleEnd],basePairs[sample2Counter][sampleStart:sampleEnd])
		if(divDO!="null"):
        		usableData.append(divDO)
        	sample2Counter+=1
        	if(sample2Counter==sample1Counter):
        		sample2Counter+=1
        		continue
        	if(sample2Counter==33):
        		sample1Counter+=1
        		sample2Counter=0
        	if(sample1Counter==33):
        		break
	if(len(usableData)>=600):
		import numpy as numpy
		fileName=sys.argv[1]
		sortData=sorted(usableData)
		size=len(sortData)
		mean=numpy.mean(usableData)
                median=numpy.median(usableData)
                standardDeviation=numpy.std(usableData)
		i=int(size*.25)
		end=int(size*.75)
		biggest_gap=0.0
		while i<end:
			if biggest_gap<sortData[i]-sortData[i-1]:
				biggest_gap=sortData[i]-sortData[i-1]
			i+=1
		if biggest_gap>median/2:
			print sys.argv[1],sampleStart,sampleEnd,biggest_gap,mean,median,standardDeviation
#		mean=numpy.mean(usableData)
#		median=numpy.median(usableData)
#		standardDeviation=numpy.std(usableData)
#		percentile10=numpy.percentile(usableData,10)
#		percentile20=numpy.percentile(usableData,20)
#		percentile30=numpy.percentile(usableData,30)
#		percentile40=numpy.percentile(usableData,40)
#		percentile50=numpy.percentile(usableData,50)
#		percentile60=numpy.percentile(usableData,60)
#		percentile70=numpy.percentile(usableData,70)
#		percentile80=numpy.percentile(usableData,80)
#		percentile90=numpy.percentile(usableData,90)
#		print("%s  %d    %d     %f    %f    %f    %f    %f    %f    %f    %f    %f    %f    %f    %f"%(fileName,sampleStart,sampleEnd,mean,median,standardDeviation,percentile10,percentile20,percentile30,percentile40,percentile50,percentile60,percentile70,percentile80,percentile90))
		#histogramData=numpy.histogram(usableData)
		#print(histogramData)
		#print(min(usableData))
		#print(max(usableData))
	sampleStart+=1000
	sampleEnd+=1000
	usableData=[]
	sample1Counter=0
	sample2Counter=1
