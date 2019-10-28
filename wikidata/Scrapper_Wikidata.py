#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import re
import bz2
import sqlite3
import logging
import logging.config
import multiprocessing
import ijson
import bs4
import requests
from wikidata.Scrapper_Wikidata_Item import WikidataItem
from Scrapper_Helpers import filterWodsProblems, clean_surrogates, pprint, create_storage, put_contents
from Scrapper_DB import DBExecute, DBExecuteScript, DBWrite
import Scrapper_Downloader

#
DB_NAME      = "wikidata.db"
DBWWikidata  = sqlite3.connect( DB_NAME, timeout=5.0 )
CACHE_FOLDER = "cached"  # folder where stored downloadad dumps
log          = logging.getLogger(__name__)

# init DB
DBExecuteScript( DBWWikidata, WikidataItem.Meta.DB_INIT )

if os.path.isfile( os.path.join( 'wikidata', 'logging.ini' ) ):
    logging.config.fileConfig( os.path.join( 'wikidata', 'logging.ini' ) )


# WikiDict dump helpers
def get_id(item, lang, default=None):
    return item.get('id', default)


def get_label(item, lang, default=None):
    try:
        return item['labels'][lang]['value']
    except KeyError:
        return default


def get_aliases(item, lang, default=None):
    try:
        aliases = item['aliases'][lang]
        aliases = [ clean_surrogates(a['value']) for a in aliases ]
    except KeyError:
        return default

    return aliases


def get_description(item, lang, default=None):
    try:
        desc = item['descriptions'][lang]['value']
    except KeyError:
        return default
    return desc


def get_site_link(item, lang, site_id, default=None):
    try:
        return item['sitelinks'][site_id]['title']
    except KeyError:
        return default


def get_wikipedia_url(item, lang, default=None):
    # case 1: url
    try:
        wikicode = lang + 'wiki'
        return item['sitelinks'][wikicode]['url']
    except KeyError:
        pass

    # case 2: title
    try:
        wikicode = lang + 'wiki'
        return "https://en.wikipedia.org/wiki/" + item['sitelinks'][wikicode]['title']
    except KeyError:
        return default


def get_properties(item , lang, prop_id, default=None):
    return item['claims'][prop_id]


def get_property_value(prop):
    return prop['mainsnak']['datavalue']['value']


def get_snak_value(snak):
    snak_type = ['snaktype']

    if snak_type == 'value':
        datavalue = snak['datavalue']
        return get_snak_value_inner(datavalue)

    elif snak_type == 'somevalue':
        return None

    elif snak_type == 'novalue':
        return None


def get_snak_value_inner(datavalue):
    value_type = datavalue['type']

    if value_type == 'string':
        return datavalue['value']

    elif value_type == 'wikibase-entityid':
        return datavalue['value']['id']

    else:
        return repr(datavalue['value'])


def get_britannica_url(item, lang, default=None):
    try:
        props = get_properties(item, lang, "P1417", default)
        return "https://www.britannica.com/" + get_property_value(props[0])
    except KeyError:
        return default


def get_universalis_url(item, lang, default=None):
    try:
        props = get_properties(item, lang, "P3219", default)
        return "https://www.universalis.fr/encyclopedie/" + get_property_value(props[0])
    except KeyError:
        return default


def get_encyclopedia_great_russian_url(item, lang, default=None):
    try:
        props = get_properties(item, lang, "P2924", default)
        return "https://bigenc.ru/" + get_property_value(props[0])
    except KeyError:
        return default


def get_instance_of(item, lang, default=None):
    try:
        result = []
        for prop in get_properties(item, lang, "P31", default):
            v = get_property_value(prop)['id']
            result.append( v )
        return result

    except KeyError:
        return default


def get_part_of(item, lang, default=None):
    try:
        result = []
        for prop in get_properties(item, lang, "P361", default):
            v = get_property_value(prop)['id']
            result.append( v )
        return result

    except KeyError:
        return default


def get_subclass_of(item, lang, default=None):
    try:
        result = []
        for prop in get_properties(item, lang, "P279", default):
            v = get_property_value(prop)['id']
            result.append( v )
        return result

    except KeyError:
        return default


def get_wikipedia_link_count_total(item, lang, default=None):
    try:
        sitelinks = item['sitelinks']
        ks = [k for k in sitelinks.keys() if k.endswith("wiki") and k != "commonswiki"]
        return len(ks)
    except KeyError:
        return default


def list_or_None(s):
    if s:
        return [s]
    else:
        return None


def get_translation(item, lang, default=None):
    return list_or_None( get_label(item, lang, None) )


# filters
def filter_label(label):
    return filterWodsProblems(label, log)


def validate_id(id_):
    # check id (required by pywikibot: Q[0-9]+)
    title_pattern = r'(Q[1-9]\d*|-1)'
    return bool( re.match(title_pattern + '$', id_) )


def validate_type(item_type):
    # check id (required by pywikibot: Q[0-9]+)
    if item_type == 'item':
        return True
    else:
        return False


# processors
def process_one(item, lang, id_, item_type, i):
    # log
    try:
        log_record = (id_, get_label(item, lang, None))
    except KeyError:
        log_record = (id_, )

    log.info(log_record)

    # id filter
    if not validate_id(id_):
        return

    # type filter
    if not validate_type(item_type):
        return

    # label filter
    label = get_label(item, lang, None)
    label = filter_label(label)
    if not label:
        return

    # miners
    aliases          = get_aliases(item, lang, None)
    desc             = get_description(item, lang, None)
    self_url         = "https://www.wikidata.org/wiki/" + id_
    wikipedia_en_url = get_wikipedia_url(item ,"en", None)
    wikipedia_fr_url = get_wikipedia_url(item ,"fr", None)
    wikipedia_de_url = get_wikipedia_url(item ,"de", None)
    wikipedia_it_url = get_wikipedia_url(item ,"it", None)
    wikipedia_es_url = get_wikipedia_url(item ,"es", None)
    wikipedia_ru_url = get_wikipedia_url(item ,"ru", None)
    wikipedia_pt_url = get_wikipedia_url(item ,"pt", None)
    britannica_url   = get_britannica_url(item ,lang, None)
    universalis_url  = get_universalis_url(item ,lang, None)
    instance_of      = get_instance_of(item ,lang, None)
    subclass_of      = get_subclass_of(item ,lang, None)
    part_of          = get_part_of(item ,lang, None)
    translation_en   = get_translation(item ,"en", None)
    translation_fr   = get_translation(item ,"fr", None)
    translation_de   = get_translation(item ,"de", None)
    translation_it   = get_translation(item ,"it", None)
    translation_es   = get_translation(item ,"es", None)
    translation_ru   = get_translation(item ,"ru", None)
    translation_pt   = get_translation(item ,"pt", None)
    wikipedia_link_count_total = get_wikipedia_link_count_total(item ,lang, None)
    encyclopedia_great_russian_url = get_encyclopedia_great_russian_url(item ,lang, None)

    w = WikidataItem()
    w.LabelName                  = label
    w.CodeInWiki                 = id_
    w.LanguageCode               = lang
    w.Description                = desc
    w.AlsoKnownAs                = aliases
    w.SelfUrl                    = self_url
    w.WikipediaENURL             = wikipedia_en_url
    w.WikipediaFRURL             = wikipedia_fr_url
    w.WikipediaDEURL             = wikipedia_de_url
    w.WikipediaITURL             = wikipedia_it_url
    w.WikipediaESURL             = wikipedia_es_url
    w.WikipediaRUURL             = wikipedia_ru_url
    w.WikipediaPTURL             = wikipedia_pt_url
    w.EncyclopediaBritannicaEN   = britannica_url
    w.EncyclopediaUniversalisFR  = universalis_url
    w.EncyclopediaGreatRussianRU = encyclopedia_great_russian_url
    w.Instance_of                = instance_of
    w.Subclass_of                = subclass_of
    w.Part_of                    = part_of
    w.Translation_EN             = translation_en
    w.Translation_FR             = translation_fr
    w.Translation_DE             = translation_de
    w.Translation_IT             = translation_it
    w.Translation_ES             = translation_es
    w.Translation_RU             = translation_ru
    w.Translation_PT             = translation_pt
    w.WikipediaLinkCountTotal    = wikipedia_link_count_total
    w.PrimaryKey                 = lang + "§" + w.LabelName + "§" + w.CodeInWiki

    return w


def process_dump_record_mp(args):
    return process_dump_record(*args)


def process_dump_record(data, lang, i):
    item = data
    id_ = data.get('id', '')
    item_type = data.get('type', '')
    return process_one(item, lang, id_, item_type, i)


def process_web_record(data, lang, id_):
    item = data['entities'][id_]
    item_type = 'item'
    process_one(item, lang, id_, item_type, 0)


# readers
def DumpReader(lang, local_file, from_point=None):
    with bz2.open(local_file, "rb") as fin:
        reader = enumerate(ijson.items(fin, "item"))

        if from_point:
            for i, data in reader:
                if data and isinstance(data, dict) and data.get('id', None) == from_point:
                    break # OK. found
                else:
                    continue

        for i, data in reader:
            yield (data, lang, i)


def find_latest_dump():
    # https://dumps.wikimedia.org/wikidatawiki/entities/
    url = "https://dumps.wikimedia.org/wikidatawiki/entities/"
    response = requests.get( url )

    soup = bs4.BeautifulSoup( response.text, "html.parser" )

    folders = []

    for a in soup.select( 'a' ):
        href =  a.attrs.get( 'href', '' ).strip()
        if href.endswith( '/' ):
            if href[:-1].isnumeric() and len( href ) == len( '19770101/' ):
                folders.append( href[:-1] )

    folders.sort()

    for folder in reversed( folders ):
        dump_url = "https://dumps.wikimedia.org/wikidatawiki/entities/{}/wikidata-{}-all.json.bz2"\
            .format( folder, folder )

        log.debug( 'check: %s', dump_url )
        response = requests.head( dump_url )

        log.debug( '  %s', response.status_code )

        if response.status_code == 200:
            return dump_url


# helpers
def download(lang="en", use_cached=True):
    """
    Download file from HTTPS.

    In:
        lang       - Language code string, like a: en, de, fr
        use_cached - True if need use cached_file. False for force run downloading.
    Out:
        local_file - local cached file name
    """
    # remote_file = 'https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2'
    # latest-all.json.bz2 - is not stable link. sometime locate to absent file. 404 - error
    # remote_file = 'https://dumps.wikimedia.org/wikidatawiki/entities/20190701/wikidata-20190701-all.json.bz2.not'
    # remote_file = 'https://dumps.wikimedia.org/wikidatawiki/entities/20190812/wikidata-20190812-all.json.bz2'
    #remote_file = 'https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2'

    # cache folder
    create_storage(CACHE_FOLDER)
    local_file = os.path.join(CACHE_FOLDER, "wikidata-latest-all.json.bz2")

    # check cache
    if use_cached and os.path.exists(local_file):
        return local_file

    # download
    remote_file = find_latest_dump()

    # keep url
    url_file_name = os.path.join( CACHE_FOLDER, "wikidata-url.txt" )
    put_contents( url_file_name, remote_file )

    log.info("Downloading (%s)....", remote_file)
    if Scrapper_Downloader.download( remote_file, local_file ):
        log.info("Downloaded... [ OK ]")
    else:
        log.error("Downloading... [ FAIL ]")
        raise Exception("Downloading... [ FAIL ]")

    return local_file


class Counter:
    unique_id = 1

    @classmethod
    def get_next_id(cls):
        cls.unique_id += 1
        return cls.unique_id


# dev helper
def check_one(id_, lang):
    # get JSOBN. https: // www.wikidata.org / w / api.php?action = parse & page = Q20152873
    import requests
    import json

    # get data from WikiDict. raw.json
    headers = {"Accept": "application/json"}
    r = requests.get("https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={}".format(id_), headers=headers)
    data = json.loads(r.text)
    pprint(data)

    # delete old record
    if os.path.isfile( DB_NAME ):
        DBExecute( DBWWikidata, "DELETE FROM wikidata WHERE CodeInWiki = ?", (id_, ))

    # process
    process_web_record(data, lang, id_)

    #log.info("All done. [ OK ]")


def scrap(lang="en", from_point=None, workers=1):
    log.info("downloading...")
    local_file = download()
    log.info("downloaded.")

    log.info("parsing...")
    if workers > 1:
        # multiprocessing
        pool = multiprocessing.Pool( workers )
        for w in pool.imap(process_dump_record_mp, DumpReader(lang, local_file, from_point)):
            if w is not None:
                DBWrite( DBWWikidata, w )

        pool.close()
        pool.join()

    else: # single process
        for (data, lang, i) in DumpReader(lang, local_file, from_point):
            w = process_dump_record(data, lang, i)
            if w is not None:
                DBWrite( DBWWikidata, w )


# main
if __name__ == "__main__":
    #check_one("Q2051873", "en")
    #check_one("Q146", "en")
    #check_one("Q147", "en")
    #check_one("Q729", "en")
    #check_one("Q4847309", "en")
    scrap("en", from_point="Q6393585")

