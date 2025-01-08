from typing import Optional

import httpx

#from models.art_model import SPARQLModel

#def get_artwork(title_subtext: str) -> Optional[SPARQLModel]:

async def get_artwork(title_subtext: str):
    #using this stack overflow approach https://stackoverflow.com/questions/55961615/how-to-integrate-wikidata-query-in-python
    url = 'https://query.wikidata.org/sparql'

    #modeled after example public art in Paris SPARQL query
    query = f"""    
SELECT ?item (SAMPLE(?titleL) AS ?title) (GROUP_CONCAT(DISTINCT ?creatorL; SEPARATOR = ", ") AS ?creator) (GROUP_CONCAT(DISTINCT ?genreL; SEPARATOR = ", ") AS ?genre) (GROUP_CONCAT(DISTINCT ?placeL; SEPARATOR = ", ") AS ?place) (GROUP_CONCAT(DISTINCT ?arr; SEPARATOR = ", ") AS ?arrondissement) (SAMPLE(?img) AS ?image) (SAMPLE(?coord) AS ?coordinates) WHERE {{
  {{
    SELECT DISTINCT ?item WHERE {{
      {{
        ?item wdt:P136 wd:Q557141;
          wdt:P131 wd:Q340.
      }}
      UNION
      {{
        ?item wdt:P136 wd:Q557141;
          (wdt:P131/(wdt:P131*)) wd:Q340.
      }}
    }}
  }}
  OPTIONAL {{   
    ?item rdfs:label ?titleL.
    FILTER CONTAINS(?titleL,"{title_subtext}")  
    FILTER((LANG(?titleL)) = "fr")
  }}
  OPTIONAL {{
    ?item wdt:P170 _:b0.
    _:b0 rdfs:label ?creatorL.
    FILTER((LANG(?creatorL)) = "fr")
  }}
  OPTIONAL {{
    {{
      ?item wdt:P136 ?g.
      FILTER((STR(?g)) != "http://www.wikidata.org/entity/Q557141")
    }}
    UNION
    {{ ?item wdt:P31 ?g. }}
    ?g rdfs:label ?genreL.
    FILTER((LANG(?genreL)) = "fr")
  }}
  OPTIONAL {{
    ?item wdt:P276 _:b1.
    _:b1 rdfs:label ?placeL.
    FILTER((LANG(?placeL)) = "fr")
  }}
  OPTIONAL {{
    ?item wdt:P131 _:b2.
    _:b2 wdt:P131 wd:Q340;
      rdfs:label ?arrL.
    FILTER((LANG(?arrL)) = "fr")
    BIND(REPLACE(?arrL, "^([0-9]+).*$", "$1", "si") AS ?arr)
  }}
  OPTIONAL {{ ?item wdt:P18 ?img. }}
  OPTIONAL {{ ?item wdt:P625 ?coord. }}
}}
GROUP BY ?item
LIMIT 1
    """

    async with httpx.AsyncClient() as client:
        resp: httpx.Response = await client.get(url, params={'format': 'json', 'query': query})
        resp.raise_for_status()

        print(resp, resp.text)

        data = resp.json()

    results = data['results']['bindings']
    if not results:
        return None

    artworks = results[0]
    #artworks = SPARQLModel(**results[0])
    return artworks