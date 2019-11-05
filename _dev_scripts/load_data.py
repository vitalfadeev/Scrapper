import os
import sqlite3
from merger.Scrapper_Merger_Item import WordItem

def load_wikidata( db_words_connection ):
    db_wikidata = "wikidata.db"

    # load data to words from wikidata
    sql = f"""
        ATTACH DATABASE "{db_wikidata}" AS db_wikidata;
    
        INSERT INTO words ( 
                PK,                
                SelfUrlWikidata,   
                LabelName,         
                LanguageCode,      
                Description,       
                AlsoKnownAs,       
                Ext_Wikipedia_URL, 
                Hypernymy,         
                Hypernymy,         
                Meronymy,          
                Translation_EN,    
                Translation_FR,    
                Translation_DE,    
                Translation_IT,    
                Translation_ES,    
                Translation_RU,    
                Translation_PT,    
                CountTotalOfWikipediaUrl,
                FromWD
            ) 
            SELECT 
                PrimaryKey as PK,                                                         
                SelfUrl as SelfUrlWikidata,                                                            
                LabelName,                                                          
                LanguageCode,                                                       
                Description,                                                        
                AlsoKnownAs,                                            
                WikipediaENURL as Ext_Wikipedia_URL,     
                Instance_of as Hypernymy,                                           
                Subclass_of as Hypernymy,                                           
                Part_of as Meronymy,                                               
                Translation_EN,                                                    
                Translation_FR,                                                    
                Translation_DE,                                                    
                Translation_IT,                                                    
                Translation_ES,                                                    
                Translation_RU,                                                    
                Translation_PT,
                WikipediaLinkCountTotal,
                PrimaryKey as FromWD                                                    
            FROM db_wikidata.wikidata;
        """

    db_words_connection.executescript( sql )


def load_conjugations( db_words_connection ):
    db_conjugations = "conjugations.db"

    # load data to words from wikidata
    sql = f"""
        ATTACH DATABASE "{db_conjugations}" AS db_conjugations;
    
        INSERT INTO words ( 
                PK,
                LabelName,
                LabelType,
                LanguageCode,
                Type,
                Description,
                AlsoKnownAs,
                RelatedTerms,
                IsMale,
                IsFeminine,
                IsSingle,
                IsPlural,
                SingleVariant,
                PluralVariant,
                IsVerbPast,
                IsVerbPresent,
                IsVerbFutur,
                FromCJ
            ) 
            SELECT 
                PK,
                LabelName,
                LabelType,
                LanguageCode,
                Type,
                ExplainationTxt as Description,
                AlternativeFormsOther as AlsoKnownAs,
                OtherwiseRelated as RelatedTerms,
                IsMale,
                IsFeminine,
                IsSingle,
                IsPlural,
                SingleVariant,
                PluralVariant,
                IsVerbPast,
                IsVerbPresent,
                IsVerbFutur,
                PK as FromCJ
            FROM db_conjugations.conjugations;
        """

    db_words_connection.executescript( sql )


if __name__ == "__main__":
    # remove old words
    db_words = "words.db"
    if os.path.isfile( db_words ): os.remove( db_words )

    # create tables
    db_words_connection = sqlite3.connect( db_words )
    db_words_connection.executescript( WordItem.Meta.DB_INIT )

    load_wikidata( db_words_connection )
    load_conjugations( db_words_connection )

