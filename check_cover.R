require("rphast")

### Set these manually ###
TTH<-5
BTH<-15
targets<-c("CollaredFlycatcher", "MediumGroundFinch", "TibetanGroundTit", "ZebraFinch", "WhiteThroatedSparrow", "Bowerbird", "AmericanCrow") 
background<-c("Mallard", "RedLeggedSerima", "GoldenEagle", "Ostrich", "Killdeer", "DownyWoodpecker", "ChuckWillsWidow", "RockDove", "GreaterPrairieChicken", "Rifleman", "BlueCrownedManakin", "CrestedIbis", "CommonCuckoo", "ChimneySwift", "AmericanFlamingo", "GoldenCollaredManakin", "EmperorPenguin", "PeregrineFalcon", "WhiteThroatedTinamous", "Hoatzin")
### End Manual Paramters ###


### Load ARGS ###
args <- commandArgs(trailingOnly = TRUE)
print(args)

# ARG[1]=bedfile
# ARG[2]=ALNfile

### LOAD DATA ###
elements <- read.feat(args[1])
elements$seqname <- "Chicken"
align <- strip.gaps.msa(read.msa(args[2], pointer.only=TRUE))

### Filter ###
hasVL <- informative.regions.msa(align, TTH, targets)
hasNVL <- informative.regions.msa(align, BTH, background)
informativeElements <- coverage.feat(elements, hasVL, hasNVL, get.feats=TRUE)

### Write to STDOUT ### 
#write(informativeElements)
informativeElements


