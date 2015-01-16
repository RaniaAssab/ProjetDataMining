
#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv

liste_interractants = {}
clusters = []

def compter_interractant_commun(liste1,liste2):
    nb =0
    for element1 in liste1:
        for element2 in liste2:
            if element1==element2:
                nb=nb+1
    return nb

def identique(element1,element2):
    test=False
    j = 0
    while j < len(element1) and test==False:
        i = 0
        
        while i < len(element2) and test==False:
            if element1[j]==element2[i]:
                test= True
            i = i +1
        j = j +1
    return test
    
def present(element,dico):
    for element_dico in dico:
        if identique(element,element_dico):
            return True
    return False

def calculer_nb_interractant_commun(prot,liste):
    interactants_prot = liste[prot]
    distance_max = 1
    liste_prot_interractants_commun=[]
    for num_access_prot in liste:
        if num_access_prot != prot:
            nb_interractant_commun = compter_interractant_commun(interactants_prot,liste[num_access_prot])
            distance_interractant_commun = ( float( max(len(interactants_prot),len(liste[num_access_prot])) - nb_interractant_commun )) / float(max(len(interactants_prot),len(liste[num_access_prot])))
            if distance_interractant_commun < distance_max:
                distance_max = distance_interractant_commun
                liste_prot_interractants_commun=[]
                liste_prot_interractants_commun.append(num_access_prot)
            elif distance_interractant_commun == distance_max:
                liste_prot_interractants_commun.append(num_access_prot)
    return liste_prot_interractants_commun,distance_max

with open('DataWareHouse_part.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar='\'')
    for row in spamreader:
        if row[0] != "Identifiant":
            liste_interractants[row[0]]=row[3]
for interractant in liste_interractants:
    cluster=[]
    cluster,valeur=calculer_nb_interractant_commun(interractant,liste_interractants)
    if not present(cluster,clusters):
        clusters.append(cluster)
        print cluster,"\n"
