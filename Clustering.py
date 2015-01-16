###############################################################################################
#####################################  DATAMINING #############################################
###############################################################################################

#Data warehouse treatment

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

cluster1 = 
for cle in DProt :
	print DProt[cle]['chainNature']



fic.close()