import numpy as np
import random

def calcul_distance(node,barycentre,param):
	somme=0
	for i in range(len(param)):
		somme = somme + pow(param[i][node] - barycentre[i],2)
	return np.sqrt(somme)
	
def calcul_barycentre(classe,param):
	barycentre = []
	for p in param:
		mean_tmp = []
		for n in classe:
			mean_tmp.append(p[n])
		barycentre.append(np.mean(mean_tmp))
	return barycentre
	
def initialisation(k,liste_interractants):
	classes=[]
	barycentres=[]
	for i in range(k):
		c1=[]
		classes.append(c1)	
		interractant = liste_interractants.pop()
		classes[i].append(interractant)
		c2=[]
		barycentres.append(c2)
		for j in range(len(param)):
			barycentres[i].append(param[j][node])
			
	while len(nodes)>0:
		node = nodes.pop()
		distance = float("inf")
		classe = -1
		for i in range (k):
			distTMP = calcul_distance(node,barycentres[i],param)
			if(distance > distTMP):
				distance = distTMP
				classe=i
		classes[classe].append(node)
		barycentres[classe]=calcul_barycentre(classes[classe],param)
	return classes,barycentres
	
def reaffectation(classes,param,barycentres):
	convergence = False
	while(not convergence):
		convergence = True
		for i in range(len(classes)):
			for node in classes[i]:
				distance = float("inf")
				classe = -1
				for j in range (len(classes)):
					distTMP = calcul_distance(node,barycentres[j],param)
					if(distance > distTMP):
						distance = distTMP
						classe=j
				if classe != i:
					classes[classe].append(node)
					classes[i].remove(node)
					barycentres[classe]=calcul_barycentre(classes[classe],param)
					barycentres[i]=calcul_barycentre(classes[i],param)
					convergence=False
	return classes
	
def estPresent(colors,r,g,v):
	for color in colors:
		if(r==color[0] and g==color[1] and v==color[2]):
			return True
	return False
	
def colorier(classes,viewColor):
	colors=[]
	for i in range(len(classes)):
		r = random.randint(0,255)
		g = random.randint(0,255)
		v = random.randint(0,255)
		while(estPresent(colors,r,g,v)):
			r = random.randint(0,255)
			g = random.randint(0,255)
			v = random.randint(0,255)
		c=[r,g,v]
		colors.append(c)
		color = tlp.Color(r,g,v)
		for node in classes[i]:
			viewColor[node]=color

def main(graph): 
    with open('DataWareHouse_part.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='|', quotechar='\'')
    for row in spamreader:
        if row[0] != "Identifiant":
            liste_interractants[row[0]]=row[3]
    k=3
	classes,barycentres=initialisation(k,liste_interractants)
	clusters=reaffectation(classes,param,barycentres)
	colorier(clusters,viewColor)
	
	
