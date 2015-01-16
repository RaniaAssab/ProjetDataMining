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
#print len(listChainNames)
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

#print occurenceCN
#print chain, signalP, initiatorM, transitP, propep, peptide

#dico = {}
#Recuperation des proteines de chaque groupe
#for occ in range(len(occurenceCN)) :
	#dico[occurenceCN[occ]] = dict()
	#for cle, valeur in DProt.items() :
	#	if DProt[cle]['chainNature'] == occurenceCN[occ] :





#CALCULS OCCURENCES DES FAMILY NAME
listFamilyName = []
for cle, valeur in DProt.items() :
	listFamilyName.append(DProt[cle]['familyName'])
#print len(listFamilyName)
occurenceFN = []
for i in range(len(listFamilyName)) :
	if not estPresent(occurenceFN, listFamilyName[i]) :
		occurenceFN.append(listFamilyName[i])
#print len(occurenceFN)


##################################
############AJOUT DE CODE LEA #########
##################################
critere1 = {}
critere2 = []
for id_prot in DProt :
	if DProt[id_prot]['chainNature'] not in critere1.keys() :
		critere1[DProt[id_prot]['chainNature']] = {}				# on initialise un dico vide pour chaque valeur de ChaineNature
	critere1[DProt[id_prot]['chainNature']][id_prot] = DProt[id_prot]	# on ajoute la proteine (definit par son identifiant) dans le dico correspondant a sa valeur de chaineNature
for chainNat in critere1 :
	critere2_interm = {}			# initialisation d'un dico intermediaire pour chaque cluster deja cree (chaque chaineNature)
	for id_prot in critere1[chainNat] :
		if critere1[chainNat][id_prot]['familyName'] not in critere2_interm.keys() :
			critere2_interm[critere1[chainNat][id_prot]['familyName']] = {}
		critere2_interm[critere1[chainNat][id_prot]['familyName']][id_prot] = critere1[chainNat][id_prot] 	# meme principe : ajout de la proteine (def par son identifiant) dnas le dico correspondant a sa valeur de familyname
	critere2.append(critere2_interm)	# ajout du dico intermediaire dans une liste, a la fin de cette etape, chaque element de la liste correspond a un cluster apres analyse des 2 premiers criteres
# test d'affichage des clusters
for dic in critere2 :
	for el in dic :
		print el + '\n'  + str(dic[el]) + '\n'

fic.close()