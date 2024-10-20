import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

# URL de la page web à scraper
url = 'https://www.bing.com/images/search?q=%D7%90%D7%AA%D7%A8%D7%95%D7%92%20%D7%9E%D7%94%D7%95%D7%93%D7%A8&qs=n&form=QBIR&sp=-1&lq=0&pq=%D7%90%D7%AA%D7%A8%D7%95%D7%92%20%D7%9E%D7%94%D7%95%D7%93%D7%A8&sc=0-11&cvid=6BEDB3C3C5734AE8A54F2491167898C9&ghsh=0&ghacc=0&first=1&adlt=strict&towww=1&redig=99836ED2A2104EDDA8ABD0CB220CE5A2'

# Envoyer une requête GET à la page web
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le contenu HTML de la page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Trouver toutes les balises qui contiennent les images des résultats de recherche
    images = soup.find_all('a', class_='iusc')  # Bing search result images are under 'a' tags with class 'iusc'

    # Créer un dossier pour sauvegarder les images
    if not os.path.exists('images'):
        os.makedirs('images')

    # Télécharger chaque image
    for img in images:
        # Les URLs des images dans les résultats sont stockés dans l'attribut "murl"
        m = img.get('m')
        if not m:
            continue

        # Extract the actual URL from the murl JSON-like string
        img_url = m.split('"murl":"')[1].split('"')[0]

        # Extraire le nom de l'image
        img_name = os.path.basename(img_url)

        try:
            # Télécharger l'image
            img_data = requests.get(img_url).content
            with open(f'images/{img_name}', 'wb') as img_file:
                img_file.write(img_data)
            print(f'{img_name} téléchargée')
        except Exception as e:
            print(f'Erreur lors du téléchargement de {img_url}: {e}')
else:
    print('La requête a échoué')
