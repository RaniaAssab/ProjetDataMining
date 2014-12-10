#classer les differentes proteines presentes dans le fichier xml en fonctions des publications en commun. 

from Bio import SeqIO
fic = open("DataWareHouse.csv", "w")
fic.write("Identifiant| Tissular et blabla \n")
fichier = open("/net/stockage/bioinfoP2015/Datamining/Projets/uniprot-reviewed_homo-sapiens.xml", "rU")

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







	fic.write(name + " | " + str(ListTissue)+ " | " + str(loca_sub) + " | " + str(interactant) + "\n")

fichier.close()
fic.close()