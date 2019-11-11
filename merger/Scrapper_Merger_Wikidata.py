import logging
import sqlite3

log = logging.getLogger(__name__)


def load_wikidata( db_words_connection ):
    log.info( "loading wikidata" )

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

                Instance_of,              
                Subclass_of,
                Part_of,
                WikipediaLinkCountTotal,

                LabelNamePreference, 
                Operation_Pref, 

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
                WikipediaLinkCountTotal as CountTotalOfWikipediaUrl,

                Instance_of,              
                Subclass_of,
                Part_of,
                WikipediaLinkCountTotal,

                LabelNamePreference, 
                Operation_Pref, 

                '["' || PrimaryKey || '"]' as FromWD                                                    
            FROM db_wikidata.wikidata;
        """

    db_words_connection.executescript( sql )


def load_wikidata_one( db_words_connection, lang, label ):
    log.info( "loading wikidata" )

    db_wikidata = "wikidata.db"

    label = label.replace("'", "''")

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
                LabelNamePreference, 
                Operation_Pref, 
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
                LabelNamePreference, 
                Operation_Pref, 

                '["' || PrimaryKey || '"]' as FromWD                                                    
            FROM db_wikidata.wikidata
           WHERE 
                 LanguageCode = '{lang}' COLLATE NOCASE
             AND LabelName = '{label}' COLLATE NOCASE;
        """

    db_words_connection.executescript( sql )


