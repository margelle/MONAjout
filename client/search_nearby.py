import requests

from art_model import ArtworkModel

def main():
    title = get_title_from_user()
    artworks: ArtworkModel = get_artworks_from_svc(title)
    if not artworks:
        print("Pas d'oeuvres trouvées!")
        return

    print(f"{artworks.title_fr} était créé par {artworks.artists[0]} dans l'année {artworks.year}!")


def get_artworks_from_svc(title):
    url = f'http://127.0.0.1:8000/api/artworks/{title}'
    resp = requests.get(url)
    resp.raise_for_status()

    return ArtworkModel(**resp.json())


def get_title_from_user():
    return input("Quel titre à chercher? ")


if __name__ == '__main__':
    main()