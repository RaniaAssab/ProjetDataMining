###############################################################################################
#####################################  DATAMINING #############################################
###############################################################################################

#Data warehouse treatment

from re import *

def estPresent(liste, elem):
	for i in range(len(liste)) :
		if elem == liste[i] :
			return True
	return False


fic = open("DataWareHouse.csv", "r")

#lines = fic.readlines()
lines = iter(fic.read().splitlines())
next(lines)  # skip first line


DProt = {}
for e in lines :
	(identifiant, tissularLocation, subcellularLocation, interactans, familyName, chainNature) = e.split("|")
	#DProt = {'identifiant' : identifiant}
	dict = {'tissularLocation' : tissularLocation, 'subcellularLocation' : subcellularLocation, 
        	'interactants' : interactans, 'familyName' : familyName, 
        	'chainNature' : chainNature
        	}
	DProt[identifiant] = dict



 ##################CLUSTER1
#CALCULS OCCURENCES DES CHAIN NATURE 1er critere
listChainNames = []
for cle, valeur in DProt.items() :
	listChainNames.append(DProt[cle]['chainNature'])
print len(listChainNames)
occurenceCN = []
for i in range(len(listChainNames)) :
	if not estPresent(occurenceCN, listChainNames[i]) :
		occurenceCN.append(listChainNames[i])
chain, signalP, initiatorM, transitP, propep, peptide = 0, 0, 0, 0, 0, 0
for i in range(len(listChainNames)) :	
	if listChainNames[i] == occurenceCN[0] :
		chain += 1
	elif occurenceCN[1] == listChainNames[i] :
		signalP += 1
	elif occurenceCN[2] == listChainNames[i] :
		initiatorM += 1
	elif match(occurenceCN[3], listChainNames[i]) :
		transitP += 1
	elif match(occurenceCN[4], listChainNames[i]) :
		propep += 1
	elif match(occurenceCN[5], listChainNames[i]) :
		peptide += 1

print occurenceCN
print chain, signalP, initiatorM, transitP, propep, peptide

dico = {}
#Recuperation des proteines de chaque groupe
for occ in range(len(occurenceCN)) :
	dico[occurenceCN[occ]] = dict()
	#for cle, valeur in DProt.items() :
	#	if DProt[cle]['chainNature'] == occurenceCN[occ] :





#CALCULS OCCURENCES DES FAMILY NAME
listFamilyName = []
for cle, valeur in DProt.items() :
	listFamilyName.append(DProt[cle]['familyName'])
print len(listFamilyName)
occurenceFN = []
for i in range(len(listFamilyName)) :
	if not estPresent(occurenceFN, listFamilyName[i]) :
		occurenceFN.append(listFamilyName[i])
print len(occurenceFN)


fic.close()