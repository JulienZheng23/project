import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://books.toscrape.com/"

def fetch_categories(session) -> list:
    """
    Récupère les catégories de livres depuis la page principale.
    """
    try:
        response = session.get(BASE_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête vers {BASE_URL} : {e}")
        raise
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.select("ul.nav.nav-list a")
    try:
        return [categorie["href"] for categorie in categories]
    except KeyError as e:
        logging.error("Impossible de trouver l'attribut <href> dans les catégories.")
        raise

def process_category(session, categorie_url: str, threshold: int) -> None:
    """
    Traite une catégorie spécifique, récupère les livres et affiche un message
    si le nombre de livres est inférieur au seuil spécifié.
    """
    full_url = urljoin(BASE_URL, categorie_url)
    try:
        response = session.get(full_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête vers {full_url} : {e}")
        raise

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select("article.product_pod")
    categorie_title = soup.select_one("h1").text
    number_of_books = len(books)

    if number_of_books <= threshold:
        logging.info(f"La catégorie {categorie_title} n'a pas assez de livres : {number_of_books}")

def main(threshold: int = 5) -> None:
    """
    Fonction principale qui gère la récupération des catégories et le traitement des livres.
    """
    with requests.Session() as session:
        categories_url = fetch_categories(session)
        for categorie_url in categories_url:
            process_category(session, categorie_url, threshold)

if __name__ == '__main__':
    main(10)
