import unicodedata
import urllib.request
import re
import time
import os

import pandas as pd

from bs4 import BeautifulSoup

link = 'https://www.cemig.com.br/atendimento/aviso-de-desligamento-programado/'
cidade = 'Alfenas'

response = urllib.request.urlopen(link)
content = response.read()

soup = BeautifulSoup(content, "html.parser", from_encoding="iso-8859-1")

links = soup.find_all('a', href=re.compile(".*docs.*")) 

if len ( links ) > 0 :

    response = urllib.request.urlopen( links[0]['href'].rstrip('edit?usp=sharing') + 'export?format=csv')
    content = response.read().decode('utf-8')

    dumpfile_path = 'dump/dump_file_' + str(time.time()).replace('.', '') + '.csv'
    dumpfile = open(dumpfile_path, 'w')
    dumpfile.write(content)
    dumpfile.close()

    df = pd.read_csv( dumpfile_path, sep=',' ).iloc[2:, 1:]
    df.columns = ['MUNICIPIO','INICIO','FIM','ENDERECOS','SITUACAO']
    df.loc[df['MUNICIPIO'].str.lower() == cidade.lower()]

    nome_cidade = unicodedata.normalize('NFD', cidade)
    nome_cidade = nome_cidade.encode('ascii', 'ignore')
    nome_cidade = nome_cidade.decode('utf-8')

    content = df.loc[df['MUNICIPIO'] == nome_cidade.upper()].to_dict()

    del df
    os.remove(dumpfile_path)

    print('Início.: ', list(content['INICIO'].values()))
    print('Fim....: ', list(content['FIM'].values()))
    print('Bairros: ', list(content['ENDERECOS'].values()))