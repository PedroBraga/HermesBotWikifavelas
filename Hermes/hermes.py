# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#BOT VERSÃO 2.1
import os.path
from datetime import date
import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import pandas as pd
from datetime import datetime
import os
from datetime import date

def raspagem_pag(link):
    main_page = urllib.request.urlopen(link)
    soup = BeautifulSoup(main_page, "lxml")
    #print(soup)
    div = soup.findAll("div", {"id":"mw-content-text"})
    return div[0]


def infos():
    A=[]

    paginas = raspagem_pag("https://wikifavelas.com.br/index.php?title=Especial:P%C3%A1ginas_novas")
    for pag in paginas.findAll("li"):
        
        
        B = "Hora/Data " + pag.find('span', { "class" : "mw-newpages-time"}).getText() + " Autor: " +  pag.find('a', { "class" : "mw-userlink"}).getText() + " Título: " + pag.find('a')['title']  + " Link: " + "https://wikifavelas.com.br/" + pag.find('a')['href'] 
        
        A.append(B)
        
     
    
    return A
                     
lista = infos()

def verifica(var):
    df = pd.read_csv("VERBETES.csv")
    listas = df["VERBETE"]
    aux = []
    retorno = [] 
    
    for y in listas:
        
        aux.append(y)
    
    for x in var:
        if x not in aux:
            
            retorno.append(x)
    Location = os.getcwd()        
    if retorno != []:
            
        BabyDataSet = list(zip(retorno))
        df2 = pd.DataFrame(data = BabyDataSet, columns=["VERBETE"])
        
        df2 = df2.append(df, ignore_index=True)
        
        df2.to_csv(Location + "VERBETES.csv", index=False)
        
        BabyDataSet2 = list(zip(retorno))
        df3 = pd.DataFrame(data = BabyDataSet2, columns=["VERBETE"])
        today = date.today()
        nome_arq_gerado = str(today)

        df3.to_csv(Location + "VERBETES_" + nome_arq_gerado.replace('-', '_') + ".csv", index=False)
        
    
    else: 
        BabyDataSet2 = list(zip(retorno))
        df3 = pd.DataFrame(data = BabyDataSet2, columns=["VERBETE"])
        today = date.today()
        nome_arq_gerado = str(today)

        df3.to_csv(Location + "VERBETES_" + nome_arq_gerado.replace('-', '_') + "_Vazio.csv", index=False)
        
    return retorno
  
def enviar(to_addrs):
    msg = MIMEMultipart()
    conteudo = verifica(lista)
    listaa = conteudo
  
    if listaa != []:
        a = "Relatório semanal de páginas novas do WIKI \n\n\n"
        for x in range(0,len(listaa)):
            a +=    listaa[x]  + "\n\n" 
        message = a
       
    else:
        print("Não há páginas novas")
        message = "Não há páginas novas."
          
    password = "5n644ndv5v33h4sj6"
    msg['From'] = "monitorverbeteswikifavelas@gmail.com"
    msg['To'] = ', '.join(to_addrs)
    today = date.today()
    msg['Subject'] = "Relatório " + str(today)
    
    msg.attach(MIMEText(message, 'plain'))

    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Login Credentials for sending the mail
    server.login(msg['From'], password)


    # send the message via the server.   msg['To'] 
    server.sendmail(msg['From'], to_addrs , msg.as_string())

    server.quit()

def confere_terca():
 
    data_atual = date.today()

    DIAS = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-Feira',
        'Sexta-feira',
        'Sábado',
        'Domingo'
    ]

    data = date(year=data_atual.year, month=data_atual.month, day=data_atual.day)
    indice_da_semana = data.weekday()
    dia_da_semana = DIAS[indice_da_semana]
    numero_dia = data.isoweekday()

    if numero_dia == 2:
        resultado = True
    else:
        resultado = False

    return(resultado)

#main
if confere_terca() == False:
    to_addrs = [ "pedrohcb@cos.ufrj.br"]#, "fornazin@gmail.com", "profsoniafleury@gmail.com", "polycarpoclara@gmail.com", "caiqueazael12@gmail.com" ]
    enviar(to_addrs)
else:
    print("Hoje não é dia de enviar o ralatório")

#Outros e-mails caso queira adicionar
# "fernando.urucu@gmail.com", "caiqueazael12@gmail.com" , "vania.dutrasmds@gmail.com", "fornazin@gmail.com", 
# "profsoniafleury@gmail.com", "polycarpoclara@gmail.com", "pallomamenezes@gmail.com" , "gabrielnunesnobre10@gmail.com", 
# "wikifavelas@gmail.com", 