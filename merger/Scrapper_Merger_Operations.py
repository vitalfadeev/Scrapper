def operation():
    # PKN preparing
    # LabelNamePreference
    ExplainationExamplesTxt = get_sentences_with_label( wd.Description, wd.LabelName )
    ExplainationTxt = wd.Description

    wds = \
        len( wd.AlsoKnownAs ) + \
        len( wd.Instance_of ) + \
        len( wd.Subclass_of ) + \
        len( wd.Part_of ) + \
        len( wd.Translation_EN ) + \
        len( wd.Translation_PT ) + \
        len( wd.Translation_DE ) + \
        len( wd.Translation_ES ) + \
        len( wd.Translation_FR ) + \
        len( wd.Translation_IT ) + \
        len( wd.Translation_RU ) + \
        math.sqrt( wd.WikipediaLinkCountTotal ) + \
        math.sqrt( len( ExplainationExamplesTxt ) ) + \
        math.sqrt( len( ExplainationTxt ) )

    # then divide by value of ( CAT-FELIDAE ) and divide by 2
    # If <0 then : =0 elif >1 then : =1

    wds = wds_value_of( 'CAT-FELIDAE' )

    if wds is None:
        return w

    #
    x = wds / wds / 2

    if x <= 0:
        w.LabelNamePreference = 0
    else:
        w.LabelNamePreference = 1

    return w
