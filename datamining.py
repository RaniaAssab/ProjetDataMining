#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################################
#####################################  DATAMINING #############################################
###############################################################################################

def chargement_DWH():
    fic = open("DataWareHouse_part.csv", "r")
    lines = iter(fic.read().splitlines())
    next(lines)  # skip first line
    DProt = {}
    for e in lines :
        (identifiant, tissularLocation, subcellularLocation, interactans, familyName, chainNature) = e.split("|")
        dict = {'tissularLocation' : tissularLocation, 'subcellularLocation' : subcellularLocation, 
                'interactants' : interactans, 'familyName' : familyName, 
                'chainNature' : chainNature
                }
        DProt[identifiant] = dict
    return DProt

# calcul barycentre
def id_median(liste_id,data,param):
    occurence_valeurs={}
    # compter les occurences
    for id_prot in liste_id:
        for valeur in data[id_prot][param]:
            if not valeur in occurence_valeurs.keys():
                occurence_valeurs[valeur] = 1
            else:
                occurence_valeurs[valeur] = occurence_valeurs[valeur]+1

    frequence_valeurs={}
    nb_prot=len(liste_id)
    moyenne = nb_prot / 2
    valeur_prot_moyenne =[]
    # calculs des frequences et création de la liste contenant les valeur du paramètre sup dont leur fréquence est supérieur à la moyenne
    for valeur in occurence_valeurs:
        frequence_valeurs[valeur] = float(occurence_valeurs[valeur]) / float(nb_prot)
        if frequence_valeurs[valeur] > moyenne:
            valeur_prot_moyenne.append(valeur)

    # recherche de la prot avec toutes ces valeurs et uniquement ces valeurs
    id_prot_moy=liste_id[0]    
    for id_prot in liste_id:
        test_prot_moy = len(data[id_prot][param])==len(valeur_prot_moyenne)
        i=0
        while test_prot_moy and i<len(data[id_prot][param]):
            j=0
            valeur_presente=False
            while not valeur_presente and j<len(valeur_prot_moyenne):
                if valeur_prot_moyenne[j] == data[id_prot][param][i]:
                    valeur_presente=True
                j = j + 1 
            if not valeur_presente:
                test_prot_moy=False                
            i = i+1
        if test_prot_moy:
            id_prot_moy = prot_id
    return id_prot_moy
    
def distance(liste_id1,liste_id2,data,param):
    id1=""
    id2=""
    if len(liste_id1)==1:
        id1=liste_id1[0]
    else:
        id1=id_median(liste_id1,data,param)
    if len(liste_id2)==1:
        id2=liste_id2[0]
    else:
        id2=id_median(liste_id2,data,param)
    similarite = 0
    for value1 in data[id1][param]:
        for value2 in data[id2][param]:
            if value1 == value2:
                similarite = similarite +1
                break
    max_len = len(data[id1][param])
    if len(data[id1][param]) < len(data[id2][param]):
        max_len = len(data[id2][param])
    distance = (float(max_len) - float(similarite)) / float(max_len)
    return distance
    
def minimum(matrice):
    i=0
    min_j=0
    min_i=0
    minimum = 1
    for i in range (len(matrice)):
        for j in range (i+1,len(matrice[i])):
            if matrice[i][j] < minimum:
                minimum = matrice[i][j]
                min_i = i
                min_j = j
    return min_i,min_j

def CAH(k,data,param,liste_id):
    ### INITIALISATION
    classes=[]
    for id_prot in liste_id:
        cluster = []
        cluster.append(id_prot)
        classes.append(cluster)

    while len(classes) > k:
        #Calcul des dissimilarités entre classes dans une matrice triangulaire supérieure
        matrice_dissim = [[1 for x in range(len(classes))] for y in range(len(classes))]
        #matrice_dissim = [[1]*len(classes)]*len(classes)
        for i in range (len(classes)):
            for j in range (i+1,len(classes)):
                matrice_dissim [i][j] = distance (classes[i],classes[j],data,param)
               
        #Recherche du minimum des dissimilarités
        i,j = minimum(matrice_dissim)
        #Fusion de classes[i] et classes[j]
        for element in classes[j]:
            classes[i].append(element)
        classes.pop(j)
    return classes

DProt = chargement_DWH()
# clustering en fonction de la nature de la chaine
print "clustering en fonction de la nature de la chaine "
critere_CN = {}
for id_prot in DProt :
    if DProt[id_prot]['chainNature'] not in critere_CN.keys() :
        critere_CN[DProt[id_prot]['chainNature']] = []                # on initialise une liste vide pour chaque valeur de ChaineNature
    critere_CN[DProt[id_prot]['chainNature']].append(id_prot)            # on ajoute la proteine (definit par son identifiant) dans le dico correspondant a sa valeur de chaineNature

# clustering en fonction de la localisation subcellulaire
print "\n clustering en fonction de la localisation subcellulaire"
critere_SCL = {}
for chainNat in critere_CN :
    k=1
    if len(critere_CN[chainNat])/100 > 0:
        k = len(critere_CN[chainNat])/100 # fixé arbitrairement
    print "groupe ",chainNat
    liste_id = []
    for id_prot in critere_CN[chainNat]:
        liste_id.append(id_prot)
    critere_SCL[chainNat] = CAH(k,DProt,"subcellularLocation",liste_id)
# vider critere_CN

# clustering en fonction des interractants
print "\n clustering en fonction des interractants"
critere_I = {}
k = 10 # fixé arbitrairement
for chainNat in critere_SCL :
    critere_I[chainNat]=[]
    for i in range (len(critere_SCL[chainNat])): # parcours clusters subcellulaires
        k=1
        if len(critere_CN[chainNat])/10 > 0:
            k = len(critere_CN[chainNat])/10 # fixé arbitrairement
        liste_id = []
        for id_prot in critere_SCL[chainNat][i]:
            liste_id.append(id_prot)
        critere_I[chainNat].append(CAH(k,DProt,"interactants",liste_id))
# vider critere_SCL

#clustering en fonction de la localisation tissulaire
print "clustering en fonction de la localisation tissulaire"
critere_TL = {}
k = 10 # fixé arbitrairement
for chainNat in critere_I :
    critere_TL[chainNat]=[]
    for i in range (len(critere_I[chainNat])): #parcours clusters subcellulaires
        listeTMP=[]
        critere_TL[chainNat].append(listeTMP)
        for j in range (len(critere_I[chainNat][i])): # parcours clusters interractants
            liste_id = []
            for id_prot in critere_SCL[chainNat][i]:
                liste_id.append(id_prot)
            critere_TL[chainNat][i].append(CAH(k,DProt,"tissularLocation",liste_id))
# vider critere_I

#clustering en fonction de la famille protéique
print "clustering en fonction de la famille protéique"
critere_FP = {}
k = 10 # fixé arbitrairement
for chainNat in critere_TL :
    critere_FP[chainNat]=[]
    for i in range (len(critere_TL[chainNat])): #parcours clusters subcellulaires
        listeTMP1=[]
        critere_FP[chainNat].append(listeTMP1)
        for j in range (len(critere_TL[chainNat][i])): # parcours clusters interractants
            listeTMP2=[]
            critere_FP[chainNat][i].append(listeTMP2)
            for k in range (len(critere_TL[chainNat][i][j])): # parcours clusters tissulaires
                dicoTMP={}
                critere_FP[chainNat][i][j].append(dicoTMP)
                for id_prot in critere_TL[chainNat][i][j][k] :
                    if DProt[id_prot]['familyName'] not in critere_FP[chainNat][i][j][k].keys() :
                        critere_FP[chainNat][i][j][k][DProt[id_prot]['familyName']]=[]
                    critere_FP[chainNat][i][j][k][DProt[id_prot]['familyName']].append(id_prot)     # meme principe : ajout de l'id de la prot dans le dico correspondant a sa valeur de familyname

# test d'affichage des clusters
for nature in critere_FP :
    for loc_cel in critere_FP[nature] :
        for interactant in loc_cel :
            for loc_tissu in interactant :
                for famille in loc_tissu :
                    print loc_tissu[famille]
                print "\n"


