## Imports ##
import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
from urllib.request import Request, urlopen

## Fonction que l'on utilisent pour récuperer les données comme on le souhaite 
def fonction(string):
    string2 = ""
    for i in range(len(string)):
        if string[i:i+1] != "\t" and string[i:i+1] != "\n" and string[i:i+1] != "\xa0":
            string2+=string[i:i+1]
    return string2

def fonction2(string):

    string2 = fonction(string)
    string3= ""
    for i in range(len(string2)):
        if string2[i] != "." and string2[i] != "€" :
            string3+=string2[i]
    return int(string3)

def fonction2bis(string):
    string2 = fonction(string)
    string3= ""
    for i in range(len(string2)):
        if string2[i] != " ":
            string3+=string2[i]
    return string3


def fonction3(text):
    L = []
    text = fonction2bis(text)
    if text.find("pièce") !=-1:
        text_p = text[0:text.find("pièce")]
        
        if text_p=="":
            L.append(0)
        else :
            L.append(int(text_p))
        
        
    char=["0","1","2","3","4","5","6","7","8","9"]
    
    if text.find("chambre") != -1:
        text_c = text[0:text.find("chambre")]
        text_c2=""
        for i in range(1, len(text_c)+1):
            if text_c[-i] in char:
                text_c2+=text_c[-i]
            else:
                break
        if text_c2=="":
            L.append(0)
        else :
            L.append(int(text_c2[::-1]))
    else :
        L.append(0)
            
    
    if text.find("m2") != -1:
        text_c3 = text[0:text.find("m2")]
        text_c4=""
        for i in range(1, len(text_c3)+1):
            if text_c3[-i] in char:
                text_c4+=text_c3[-i]
            else:
                break
        if text_c4=="":
            L.append(0)
        else :
            L.append(int(text_c4[::-1]))
    else :
        L.append(0)
    return L

def fonction4(string4):
    string5=fonction(string4)
    string6=""
    
    if string5.find("Paris")!= -1:
        string6+='Paris'
    elif string5.find("Marseille")!= -1:
        string6+='Marseille'
    elif string5.find("Lyon")!= -1:
        string6+='Lyon'
    elif string5.find("Toulouse")!= -1:
        string6+='Toulouse'
    elif string5.find("Nice")!= -1:
        string6+='Nice'
    elif string5.find("Nantes")!= -1:
        string6+='Nantes'
    elif string5.find("Montpellier")!= -1:
        string6+='Montpellier'
    elif string5.find("Strasbourg")!= -1:
        string6+='Strasbourg'
    elif string5.find("Bordeaux")!= -1:
        string6+='Bordeaux'
    elif string5.find("Lille")!= -1:
        string6+='Lille'
    return string6
    
    
    

def fonction5(string7):
    string8=fonction(string7)
    string9=""
    #Paris
    if string8.find("Paris")!= -1:
        if string8.find("(75000)")!= -1:
            string9+='75000'
        elif string8[string8.find("1")]=='1'and string8[string8.find("1")+1]=='E':
            string9+='75001'
        elif string8[string8.find("2")]=='2'and string8[string8.find("2")+1]=='E':
            string9+='75002'
        elif string8[string8.find("3")]=='3'and string8[string8.find("3")-1]==' ':
            string9+='75003'
        elif string8[string8.find("4")]=='4'and string8[string8.find("4")-1]==' ':
            string9+='75004'
        elif string8[string8.find("5")]=='5'and string8[string8.find("5")-1]==' ':
            string9+='75005'
        elif string8[string8.find("6")]=='6'and string8[string8.find("6")-1]==' ':
            string9+='75006'
        elif string8[string8.find("7")]=='7'and string8[string8.find("7")-1]==' ':
            string9+='75007'
        elif string8[string8.find("8")]=='8'and string8[string8.find("8")-1]==' ':
            string9+='75008'
        elif string8[string8.find("9")]=='9'and string8[string8.find("9")-1]==' ':
            string9+='75009'
        elif string8[string8.find("10")]=='1' and string8[string8.find("10")+1]=='0':
            string9+='75010'
        elif string8[string8.find("11")]=='1' and string8[string8.find("11")+1]=='1':
            string9+='75011'
        elif string8[string8.find("12")]=='1' and string8[string8.find("12")+1]=='2':
            string9+='75012'
        elif string8[string8.find("13")]=='1' and string8[string8.find("13")+1]=='3':
            string9+='75013'
        elif string8[string8.find("14")]=='1' and string8[string8.find("14")+1]=='4':
            string9+='75014'
        elif string8[string8.find("15")]=='1' and string8[string8.find("15")+1]=='5':
            string9+='75015'
        elif string8[string8.find("16")]=='1' and string8[string8.find("16")+1]=='6':
            string9+='75016'
        elif string8[string8.find("17")]=='1' and string8[string8.find("17")+1]=='7':      
            string9+='75017'
        elif string8[string8.find("18")]=='1' and string8[string8.find("18")+1]=='8':
            string9+='75018'
        elif string8[string8.find("19")]=='1' and string8[string8.find("19")+1]=='9':
            string9+='75019'
        elif string8[string8.find("20")]=='2' and string8[string8.find("20")+1]=='0':
            string9+='75020'


     #Bordeaux   
    elif string8.find("Bordeaux")!= -1:        
        if string8.find("(33000)")!= -1:
            string9+='33000'
        elif string8.find("(33100)")!= -1:
            string9+='33100'
        elif string8.find("(33200)")!= -1:
            string9+='33200'
        elif string8.find("(33300)")!= -1:
            string9+='33300'
        elif string8.find("(33800)")!= -1:
            string9+='33800'

                         
            
            
     #Lille       
    elif string8.find("Lille")!= -1:            
        if string8.find("(59000)")!= -1:
            string9+='59000'
        elif string8.find("(59160)")!= -1:
            string9+='59160'
        elif string8.find("(59260)")!= -1:
            string9+='59260'
        elif string8.find("(59800)")!= -1:
            string9+='59800'

     #Lyon
    elif string8.find("Lyon")!= -1: 
        if string8.find("(69000)")!= -1:
            string9+='69000'
        if string8.find("1Er")!= -1:
            string9+='69001'
        elif string8.find("2E")!= -1:
            string9+='69002'
        elif string8.find("3E")!= -1:
            string9+='69003'
        elif string8.find("4E")!= -1:
            string9+='69004'
        elif string8.find("5E")!= -1:
            string9+='69005'
        elif string8.find("6E")!= -1:
            string9+='69006'
        elif string8.find("7E")!= -1:
            string9+='69007'
        elif string8.find("8E")!= -1:
            string9+='69008'
        elif string8.find("9E")!= -1:
            string9+='69009'

         #Marseille   
    elif string8.find("Marseille")!= -1:
        if string8.find("(13000)")!= -1:
            string9+='13000'
        elif string8.find("1Er")!= -1:
            string9+='13001'
        elif string8.find("2E")!= -1:
            string9+='13002'
        elif string8.find("3E")!= -1:
            string9+='13003'
        elif string8.find("4E")!= -1:
            string9+='13004'
        elif string8.find("5E")!= -1:
            string9+='13005'
        elif string8.find("6E")!= -1:
            string9+='13006'
        elif string8.find("7E")!= -1:
            string9+='13007'
        elif string8.find("8E")!= -1:
            string9+='13008'
        elif string8.find("9E")!= -1:
            string9+='13009'
        elif string8[string8.find("10")]=='1' and string8[string8.find("10")+1]=='0':
            string9+='13010'
        elif string8[string8.find("11")]=='1' and string8[string8.find("11")+1]=='1':
            string9+='13011'
        elif string8[string8.find("12")]=='1' and string8[string8.find("12")+1]=='2':
            string9+='13012'
        elif string8[string8.find("13")]=='1' and string8[string8.find("13")+1]=='3':
            string9+='13013'
        elif string8[string8.find("14")]=='1' and string8[string8.find("14")+1]=='4':
            string9+='13014'
        elif string8[string8.find("15")]=='1' and string8[string8.find("15")+1]=='5':
            string9+='13015'
        elif string8[string8.find("16")]=='1' and string8[string8.find("16")+1]=='6':
            string9+='13016'        
     
        
        
        
       #Nantes 
    elif string8.find("Nantes")!= -1:                         
        if string8.find("(44000)")!= -1:
            string9+='44000'
        elif string8.find("(44100)")!= -1:
            string9+='44100'
        elif string8.find("(44200)")!= -1:
            string9+='44200'
        elif string8.find("(44300)")!= -1:
            string9+='44300'

                
       #Montpellier     
    elif string8.find("Montpellier ")!= -1:          
        if string8.find("(34000)")!= -1:
            string9+='34000'
        elif string8.find("(34070)")!= -1:
            string9+='34070'
        elif string8.find("(34080)")!= -1:
            string9+='34080'
        elif string8.find("(34090)")!= -1:
            string9+='34090'
  

     #Nice       
    elif string8.find("Nice")!= -1:          
        if string8.find("(06000)")!= -1:
            string9+='06000'
        elif string8.find("(06100)")!= -1:
            string9+='06100'
        elif string8.find("(06200)")!= -1:
            string9+='06200'
        elif string8.find("(06300)")!= -1:
            string9+='06300'            

     #Toulouse       
    elif string8.find("Toulouse")!= -1:          
        if string8.find("(31000)")!= -1:
            string9+='31000'
        elif string8.find("(31100)")!= -1:
            string9+='31100'
        elif string8.find("(31200)")!= -1:
            string9+='31200'
        elif string8.find("(31300)")!= -1:
            string9+='31300'
        elif string8.find("(31400)")!= -1:
            string9+='31400'
        elif string8.find("(31500)")!= -1:
            string9+='31500'
     
            
     #Strasbourg       
    elif string8.find("Strasbourg")!= -1:          
        if string8.find("(67000)")!= -1:
            string9+='06000'
        elif string8.find("(67100)")!= -1:
            string9+='06100'
        elif string8.find("(67200)")!= -1:
            string9+='06200'          
 
    
    else:
        string9+=""
    return(string9)
            
        
                    
        
        
        
        

    
    

## Url des pages que l'on veut scrapper 

url="https://www.pap.fr/annonce/vente-appartement-maison-paris-75-g439-"
url2="https://www.pap.fr/annonce/vente-appartement-maison-marseille-13-g12024-"
url3="https://www.pap.fr/annonce/vente-appartement-maison-lyon-69-g43590-"
url4="https://www.pap.fr/annonce/vente-appartement-maison-toulouse-31-g43612-"
url5="https://www.pap.fr/annonce/vente-appartement-maison-nice-06-g8979-"
url6="https://www.pap.fr/annonce/vente-appartement-maison-nantes-44-g43619-"
url7="https://www.pap.fr/annonce/vente-appartement-maison-montpellier-34-g43621-"
url8="https://www.pap.fr/annonce/vente-appartement-maison-strasbourg-67-g43623-"
url9="https://www.pap.fr/annonce/vente-appartement-maison-bordeaux-33-g43588-"
url10="https://www.pap.fr/annonce/vente-appartement-maison-lille-59-g43627-"



URL=[url,url2,url3,url4,url5,url6,url7,url8,url9,url10]

##### Début du scrapping avec BeautifulSoup #### 

scrapping=[]
for ur in URL:
     for k in range (1,21):
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(ur+str(k),headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page)
        for i in soup.find_all(class_="item-body"):
            scrap={}
            lieux=i.find_all(class_="h1")
            prix=i.find_all(class_="item-price")
            description=i.find_all(class_="item-description")
            taille=i.find_all(class_="item-tags")
            for localisation in lieux:
                if localisation.text[0]=="P" or localisation.text[0]=="M" or localisation.text[0]=="L" or localisation.text[0]=="T" or localisation.text[0]=="N" or localisation.text[0]=="S" or localisation.text[0]=="B":
                    scrap['lieux']=fonction(localisation.text)
            
                    scrap['Ville']=fonction4(localisation.text)
                    scrap['code postal']=fonction5(localisation.text)
                    for price in prix:
                        scrap['prix']=fonction2(price.text)
                    for mcarre in taille:
                        L = fonction3(fonction(mcarre.text))
                        if len(L)!=3:
                            L=[0,0,0]
                 
                        else:
                            
                            scrap['pièce']=L[0]
                            scrap['chambre']=L[1]
                            scrap['m2']=L[2]

                    scrapping.append(scrap)

# On supprime les valeurs dupliquée 
seen = set()
new_scrapping = []
for d in scrapping:
    t = tuple(d.items())
    if t not in seen:
        seen.add(t)
        new_scrapping.append(d)
        
## Mise en format json de nos données scrapées        
import json
with open ("scrapping.json", "w") as projet:
    json.dump(new_scrapping,projet)


