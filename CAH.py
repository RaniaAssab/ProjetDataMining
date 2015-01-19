#!/usr/bin/python
# -*- coding: utf-8 -*-
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


data = chargement_DWH()
k = 10
liste_id = []
for key in data:
    liste_id.append(key)
param="subcellularLocation"

#tissularLocation
#interactants
clusters = CAH(k,data,param,liste_id)
for cluster in clusters:
    print cluster,"\n"