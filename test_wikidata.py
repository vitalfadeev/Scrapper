from wikidata import Scrapper_Wikidata


if __name__ == "__main__":
    Scrapper_Wikidata.scrap( 'en', workers=1, from_point="Q6027695" )

