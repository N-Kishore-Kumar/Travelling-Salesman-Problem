import time
from math import ceil, exp
from random import choice, shuffle,randint
import matplotlib.pyplot as plt
import numpy as np

def second(a):
	return a[1]

def fitness(ck,dismat):
	dis=0
	for i in range(l-1):
		dis=dis+dismat[ck[0][i]][ck[0][i+1]]
	fit=1/dis
	return fit

'''
def fitness2(ck,dismat):
	dis=0
	for i in range(l-1):
		dis=dis+dismat[ck[i]][ck[i+1]]
	fit=1/dis
	return fit
'''
def distanc(ck,dismat):
	dis=0
	for i in range(l-1):
		dis=dis+dismat[ck[i]][ck[i+1]]
	return dis

def swappa(a1,b1,r1):
	for k in range(r1):
		 #print(k)
		 ind=b1.index(a1[k])
		 b1[ind]=b1[k]
		 b1[k]=a1[k]
	
	return b1
		



def three_opt(route):
	best1 = route
	improved = True
	while (improved):
		improved = False
		for q in range(1, len(route)-2):
			for e in range(q+1,len(route)-1):
				for t in range(e+1,len(route)):
					if t-e==1: continue
					new_route = route[:q]+route[q:e][::-1] + route[e:t][::-1] + route[t:]
					if distanc(new_route,dismat) < distanc(best1,dismat):
						best1 = new_route
						improved = True
						route = best1
	return best1


	

starttime=time.time()
n=100
#Defining number of roosters, hens and chicks
rn=ceil(0.02*n)
hn=ceil(0.2*n)
cn=n-rn-hn
mn=ceil(0.05*n)
g=2
iteration=50


INF = 100000000
f=open("eil51.txt","r")
a=[]
l=f.read()

#Converting the dataset into a single list
a=l.split()
x=[]
cor=[]
k=0

#Separating the list into list of each elements
for i in range(0,len(a)):
	if(k==3):
		cor.append(x)
		k=1
		x=[]
		x.append(float(a[i]))
	else:
		x.append(float(a[i]))
		k+=1
cor.append(x)

#Computing Distance of each pairs of points given in the dataset
dismat=[]
for i in range(0,len(cor)):
	dista=[]
	for j in range(0,len(cor)):
		if i==j:
			dista.append(INF)
		else:
			dist=round((((cor[i][1]-cor[j][1])**2)+((cor[i][2]-cor[j][2])**2))**0.5,4)
			dista.append(dist)
	dismat.append(dista)

l=len(dismat)

chicken=[]
for i in range(l):
	chicken.append(i)
chicken2=[]
for i in range(n):
	shuffle(chicken)
	a=chicken.copy()
	chicken2.append([a])

#Calculating the fitness value of each pairs of points 	
for i in range(n):
	dis=0
	for j in range(l-1):
		dis=dismat[chicken2[i][0][j]][chicken2[i][0][j+1]]
	fit=1/dis
	chicken2[i].append(fit)
	

for i in range(n):
	chicken2[i].append([])
	chicken2[i].append([])
    
#Defining the relaion between roosters, hens and chics
def relation(chicken2,rn,hn,cn,mn,n):
	chicken2.sort(reverse=True,key=second)
	rooster=chicken2[:rn]
	hens=chicken2[rn:(hn+rn)]
	chicks=chicken2[(hn+rn):]
	shuffle(hens)
	mothers=hens[:mn]
	for i in range(rn):
		rooster[i][2]=[]
		rooster[i][3]=[]
	for i in range(hn):
		temp=choice(rooster)
		temp2=choice(rooster)
		hens[i][2]=temp[0]
		hens[i][3]=temp2[0]
	for i in range(cn):
		temp1=choice(mothers)
		chicks[i][2]=temp1[0]
		chicks[i][3]=temp1[2]
	return rooster,hens,chicks

#Defining the movement of rooster, hens and chicks
best=[]
bestfit=0
for t in range(iteration):
	if t%g==0:
		rooster,hens,chicks=relation(chicken2,rn,hn,cn,mn,n)
		if(rooster[0][1]>bestfit):
			best=rooster[0][0].copy()
			bestfit=rooster[0][1]
	
	for i in rooster:
		ran=randint(1,ceil(l/10))
		for j in range(ran):
			temp=randint(0,l-1)
			temp1=randint(0,l-1)
			temp2=i[0][temp]
			i[0][temp]=i[0][temp1]
			i[0][temp1]=temp2
		i[0]=three_opt(i[0])
		i[1]=fitness(i,dismat)
		if(i[1]>bestfit):
			bestfit=i[1]
			best=i[0].copy()
	for i in hens:
		if(i[0]!=i[2]):
			ran=randint(ceil(l/10),ceil(l/3))
			
			i[0]=swappa(i[2],i[0],ran)
		if(i[0]!=i[3]):
			ran=randint(ceil(l/20),ceil(l/10))
			i[0]=swappa(i[3],i[0],ran)
		i[1]=fitness(i,dismat)
		if(i[1]>bestfit):
			bestfit=i[1]
			best=i[0].copy()
	for i in chicks:
		c=4
		fl=9
		if(i[0]!=i[2]):
			i[0]=swappa(i[2],i[0],c)
		if(i[0]!=i[3]):
			i[0]=swappa(i[3],i[0],fl)
		i[1]=fitness(i,dismat)
		if(i[1]>bestfit):
			bestfit=i[1]
			best=i[0].copy()
            
#Finding the best distance and corresponding time taken
best=three_opt(best)
print('Path:',best)
ml=len(best)-1
bdis=distanc(best,dismat)
bdis=bdis+dismat[best[ml]][best[0]]
print('Best distance: ',bdis)
timetaken=time.time()-starttime
print('Time Taken:',timetaken)
path=best
xp=[]
yp=[]
for i in range(len(path)):
	xp.append(cor[path[i]][1])
	yp.append(cor[path[i]][2])
xp.append(cor[path[0]][1])
yp.append(cor[path[0]][2])
plt.plot(xp,yp,ls="--",marker='o')
plt.show()

