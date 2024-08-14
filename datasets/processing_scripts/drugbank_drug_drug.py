import os
import pandas as pd
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("../data/drugbank/full database.xml"),"xml")
drugs_xml = soup.findAll("drug")

sep = ","
with open('interactions_edges.txt', 'w') as f:
    for drug in soup.findAll("drug"):
        drugName = drug.find("drugbank-id").text
        interactions = drug.findAll("drug-interaction")
        if not interactions:
            continue
        for i in interactions:
            toPrint = drugName + sep + i.find("drugbank-id").text + '\n'
            f.write(toPrint)
            
pd.read_csv('interactions_edges.txt', names=['drug1','drug2']).to_csv('../data/drugbank/drug_drug.csv', index=False)

os.remove('interactions_edges.txt')


all_drugids = []
all_atc_codes = []

for drug in drugs_xml:
    drugid = drug.find("drugbank-id").text
    if drug.find("atc-code") is not None:
        atcs = drug.find("atc-code")
        atc_codes = atc.attrs['code']
    else:
        atc_codes = None

    all_drugids.append(drugid)
    all_atc_codes.append(atc_codes)

drugbank_atc_codes = pd.DataFrame({
    'drugbank_id':all_drugids,
    'atc_codes':all_atc_codes,
})

drugbank_atc_codes.to_csv('../data/vocab/drugbank_atc_codes.csv')
