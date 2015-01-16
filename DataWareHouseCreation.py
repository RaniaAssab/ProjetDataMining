#classer les differentes proteines presentes dans le fichier xml en fonctions des publications en commun. 

from re import *
import string

from Bio import SeqIO

###############################################################################################
##############################  DATA WHAREHOUSE CREATION ######################################
###############################################################################################

print "Data WareHouse Creation"

fic = open("DataWareHouse.csv", "w")

print "Pending"

fic.write("Identifiant| Tissular Location | Subcellular Location | Interactans | Family name | Chain Nature \n")
fichier = open("/autofs/netapp/account/cremi/ranassab/espaces/travail/uniprot-reviewed_homo-sapiens.xml", "rU")

for record in SeqIO.parse(fichier, "uniprot-xml"):
	ListTissue = []

	# critere ID
	name = record.name



	# Critere : tissu
	for ref in record.annotations['references'] :
		elem = ref.comment.split(" | ")
		if elem[-1] != "" : #-1 correspond au dernier
			ListTissue.append(elem[-1][8:])

	# critere localisation subcellulaire
	if record.annotations.has_key('comment_subcellularlocation_location'):
		loca_sub = record.annotations['comment_subcellularlocation_location']
	else :
		loca_sub = []

	# critere interaction : id liste des interactants
	if record.annotations.has_key('comment_interaction_intactId'):
		inter = record.annotations['comment_interaction_intactId']
		for i in range(len(inter)):
			#name = inter[0]
			interactant = inter[1:]
	else :
		inter = []

	# critere nature de la chaine proteique:
	typeChain = record.features[0].type
	

	#nom principal de la proteine
	description = record.description
	elemDecsrpt = description.split(" ")
	descrpt = ''

	if len(elemDecsrpt) >= 3 :
		for i in range(3) :
			expression1 = r"^[0-9][A-Z]$"
			expression2 = r"^[0-9]$"
			expression3 = r"^[A-Z][0-9]$"
			expression4 = r"^[A-Z]$"
			if search(expression1, elemDecsrpt[i]) or search(expression2, elemDecsrpt[i]) or search(expression3, elemDecsrpt[i]) or search(expression4, elemDecsrpt[i]) :
				pass
			else :
				descrpt += elemDecsrpt[i]
				descrpt += ' '


	fic.write(name + " | " + str(ListTissue)+ " | " + str(loca_sub) + " | " + str(interactant) + " | " + str(descrpt) + " | " + str(typeChain) + "\n")
fichier.close()
fic.close()

print "Done!"


###############################################################################################
###############################################################################################
###############################################################################################