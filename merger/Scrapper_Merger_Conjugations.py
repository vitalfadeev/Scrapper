import logging

log = logging.getLogger(__name__)


def load_conjugations( db_words_connection ):
    log.info( "loading conjugations" )

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
                LabelNamePreference, 
                Operation_Pref, 
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
                LabelNamePreference, 
                Operation_Pref, 

                '["' || PK || '"]' as FromCJ 
            FROM db_conjugations.conjugations;
        """

    db_words_connection.executescript( sql )


def load_conjugations_one( db_words_connection, lang, label ):
    log.info( "loading conjugations" )

    db_conjugations = "conjugations.db"

    label = label.replace('\'', '\'\'')

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
                LabelNamePreference, 
                Operation_Pref, 
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
                LabelNamePreference, 
                Operation_Pref, 
                '["' || PK || '"]' as FromCJ 
            FROM db_conjugations.conjugations
           WHERE 
                 LanguageCode = '{lang}' COLLATE NOCASE
             AND LabelName = '{label}' COLLATE NOCASE;
        """

    db_words_connection.executescript( sql )
