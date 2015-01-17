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
critere_CN = {}
critere_FN = []
for id_prot in DProt :
	if DProt[id_prot]['chainNature'] not in critere_CN.keys() :
		critere_CN[DProt[id_prot]['chainNature']] = []				# on initialise une liste vide pour chaque valeur de ChaineNature
	critere_CN[DProt[id_prot]['chainNature']].append(id_prot)			# on ajoute la proteine (definit par son identifiant) dans le dico correspondant a sa valeur de chaineNature
for chainNat in critere_CN :
	critere_FN_interm = {}			# initialisation d'un dico intermediaire pour chaque cluster deja cree (chaque chaineNature)
	for id_prot in critere_CN[chainNat] :
		if DProt[id_prot]['familyName'] not in critere_FN_interm.keys() :
			critere_FN_interm[DProt[id_prot]['familyName']] = []
		critere_FN_interm[DProt[id_prot]['familyName']].append(id_prot) 	# meme principe : ajout de l'id de la prot dans le dico correspondant a sa valeur de familyname
	critere_FN.append(critere_FN_interm)	# ajout du dico intermediaire dans une liste, a la fin de cette etape, chaque element de la liste correspond a un cluster apres analyse des 2 premiers criteres
# test d'affichage des clusters
for dic in critere_FN :
	for el in dic :
		print el + '\n'  + str(dic[el]) + '\n'

fic.close()