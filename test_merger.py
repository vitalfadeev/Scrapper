if __name__ == "__main__":
    # Scrap all pages
    import os
    if os.path.isfile("word.db"): os.remove("word.db")

    from merger import Scrapper_Merger
    Scrapper_Merger.main()

