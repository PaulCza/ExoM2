from email.headerregistry import Address
import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import time
from geopy.geocoders import OpenCage
## Accès au site web
request = requests.get('https://www.leportagesalarial.com/coworking/')
soup = BeautifulSoup(request.content, 'html.parser')

#Délimitation du contenu
idf = soup.find('h3', string=re.compile("Coworking Paris"))
notidf = soup.find('a', string=re.compile("La Rochelle"))

#Mise de tous les liens d'IDF dans une liste
liens = []
for i in idf.find_all_next('a', href=True):
    if i == notidf:
        break
    liens.append(i['href'])

#print(liens) print de debug


# Création de deux listes pour les noms et les coordonnées
coordonnees = []
noms = []

# Récupération des noms et des coordonnées
for i in liens:
    response = requests.get(i)
    page_content = BeautifulSoup(response.content, 'html.parser')
    #Récupération du nom
    header_content = page_content.find(class_='penci-page-header').get_text()
    header_content = header_content.split(':')[0]
    header_content = header_content.replace('\n', '')
    noms.append(header_content)
    print(header_content)

    #Récupération du reste des coordonnées
    adresse = page_content.find(string=re.compile("Contacter"))
    if adresse:
        adresse = adresse.find_next().get_text()
    else:
        adresse = page_content.find(string=re.compile("A propos de")).find_next().get_text()
    coordonnees.append(adresse)

    #Ligne de debug pour vérifier que le programme est en cours
    print("En cours")

#print(noms)
#print(coordonnees) prints de debug

# Tri des coordonnées en champs
details = []
for i in coordonnees:
    detail = {
        'Adresse': '',
        'Telephone': '',
        'Acces': '',
        'Site': '',
        'Twitter': '',
        'Facebook': '',
        'Linkedin': ''
    }
    if "Adresse :" in i:
        start = i.find("Adresse :") + len("Adresse :")
        end = i.find('\n', start)
        detail['Adresse'] = i[start:end].strip()
    if "Téléphone :" in i:
        start = i.find("Téléphone :") + len("Téléphone :")
        end = i.find('\n', start)
        detail['Telephone'] = i[start:end].strip()
    if "Accès :" in i:
        start = i.find("Accès :") + len("Accès :")
        end = i.find('\n', start)
        detail['Acces'] = i[start:end].strip()
    if "Site :" in i:
        start = i.find("Site :") + len("Site :")
        end = i.find('\n', start)
        detail['Site'] = i[start:end].strip()
    if "Twitter :" in i:
        start = i.find("Twitter :") + len("Twitter :")
        end = i.find('\n', start)
        detail['Twitter'] = i[start:end].strip()
    if "Facebook :" in i:
        start = i.find("Facebook :") + len("Facebook :")
        end = i.find('\n', start)
        detail['Facebook'] = i[start:end].strip()
    if "Linkedin :" in i:
        start = i.find("Linkedin :") + len("Linkedin :")
        end = i.find('\n', start)
        detail['Linkedin'] = i[start:end].strip()
    details.append(detail)

# création du fichier CSV
csv_file_path = './details.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Nom', 'Adresse', 'Telephone', 'Acces', 'Site', 'Twitter', 'Facebook', 'Linkedin']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for nom, detail in zip(noms, details):
        row = {'Nom': nom}
        row.update(detail)
        writer.writerow(row)


# Nettoyage du CSV
df = pd.read_csv(csv_file_path)

# Suppression des doublons
df_cleaned = df.drop_duplicates()
# Suppression des lignes avec des valeurs manquantes en nom ou adresse
df_cleaned = df_cleaned.dropna(subset=['Nom', 'Adresse'])

# suppression des espaces vides
df_cleaned = df_cleaned.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Sauvegarde
df_cleaned.to_csv(csv_file_path, index=False)



#Début de la géocodification

# utilisation de Geocode (clé api pas liée à un paiement donc osef)
geolocator = OpenCage("9f92dd12661847e89ff4e912fa43b72b")  # Replace with your OpenCage API key

# lecture du fichier CSV
df_cleaned = pd.read_csv(csv_file_path)

# Initialisation des listes
latitudes = []
longitudes = []

# Geocode chaque adresse
for address in df_cleaned['Adresse']:
    location = geolocator.geocode(address)
    if location:
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
    else:
        latitudes.append(None)
        longitudes.append(None)
    time.sleep(1)  # A cause des limites de l'API

# ajout des coordonnées au csv
df_cleaned['Latitude'] = latitudes
df_cleaned['Longitude'] = longitudes

# Sauvegarde du CSV
df_cleaned.to_csv(csv_file_path, index=False)
