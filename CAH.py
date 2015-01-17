import math

def chargement_DWH():
    fic = open("DataWareHouse_part.csv", "r")
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
    return DProt

# calcul barycentre
def id_median(liste_id,data):
    

def distance(liste_id1,liste_id2,data,param):
    id1=""
    id2=""
    if len(liste_id1)==1:
        id1=liste_id1[0]
    else:
        id1=id_median(liste_id1,data)
    if len(liste_id2)==1:
        id2=liste_id2[0]
    else:
        id2=id_median(liste_id2,data)
    similarite = 0
    for value1 in data[id1][param]:
        for value2 in data[id2][param]:
            if value1 == value2:
                similarite = similarite +1
    distance = (max((len(data[id1][param]),len(data[id2][param])) - similarite) / max((len(data[id1][param]),len(data[id2][param]))
    return distance
    
def minimum(matrice):
    i=0
    min_j=0
    min_i=0
    minimum = 1
    while i<len(matrice):
        j=i+1
        while j<len(matrice[i]):
            if matrice[i][j] < minimum:
                minimum = matrice[i][j]
                min_i = i
                min_j = j
            j=j+1
        i=i+1
    return min_i,min_j

### INITIALISATION
data = chargement_DWH()
classes=[]
k = 5
for id_prot in liste_id:
  classes.append(list(id_prot))


while len(classes) > k:
    #Calcul des dissimilarités entre classes dans une matrice triangulaire supérieure
    matrice_dissim = [[1]*len(classes)]*len(classes)
    for i in range (len(classes)):
        for j in range (i+1,len(classes)):
            matrice_dissim [i][j] = distance (classes[i],classes[j],data,param)
    #Recherche du minimum des dissimilarités
    i,j = minimum(matrice_dissim)
    #Fusion de classes[i] et classes[j]
    for element in classes[j]:
        classes[i].append(element)
    classes.pop(j)

