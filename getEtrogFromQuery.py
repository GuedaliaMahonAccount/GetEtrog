import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin


def fetch_etrog_images(query, num_images=500):
    url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the correct images in search results (high-res versions)
    images = soup.find_all('a', class_='iusc', limit=num_images)

    if not os.path.exists('etrog_images'):
        os.makedirs('etrog_images')

    for i, img in enumerate(images):
        try:
            # Extract the actual image URL (stored in 'murl' within a tag's attribute)
            m = img.get('m')
            img_url = m.split('"murl":"')[1].split('"')[0]

            # Fetch the image content
            img_data = requests.get(img_url).content
            with open(f'etrog_images/etrog_{i + 1}.jpg', 'wb') as handler:
                handler.write(img_data)
            print(f"Image {i + 1} téléchargée.")
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {i + 1}: {e}")


fetch_etrog_images('etrogim', num_images=500)
