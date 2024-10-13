import requests
from bs4 import BeautifulSoup
import re
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://books.toscrape.com/"

def fetch_one_star_books(session) -> list:
    """
    Récupère les liens des livres ayant une étoile depuis la page principale.
    """
    book_ids = []

    try:
        response = session.get(BASE_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de la requête vers {BASE_URL} : {e}")
        raise

    soup = BeautifulSoup(response.text, "html.parser")
    one_star_books = soup.select("p.star-rating.One")

    for book in one_star_books:
        try:
            book_link = book.find_next("h3").find("a")["href"]
        except AttributeError as e:
            logging.error("Impossible de trouver la balise <h3> : %s", e)
            raise
        except TypeError as e:
            logging.error("Impossible de trouver la balise <a> : %s", e)
            raise
        except KeyError as e:
            logging.error("Impossible de trouver l'attribut <href> : %s", e)
            raise

        try:
            book_id = re.findall(r"_\d{1,}", book_link)[0][1:]
            logging.info(f"ID du livre récupéré : {book_id}")
        except IndexError as e:
            logging.error("Impossible de retrouver l'ID du livre : %s", e)
            raise
        else:
            book_ids.append(book_id)

    return book_ids

def main() -> None:
    """
    Fonction principale qui gère la récupération des livres avec une étoile.
    """
    with requests.Session() as session:
        book_ids = fetch_one_star_books(session)
        if book_ids:
            logging.info(f"Livres récupérés avec 1 étoile : {book_ids}")
        else:
            logging.info("Aucun livre avec une étoile trouvé.")

if __name__ == '__main__':
    main()
