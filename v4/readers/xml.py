from lxml import etree

# XmlStreamReader(xml_stream)

def Reader( f, stream=False ):
    if stream:
        stream = etree.iterparse( f, huge_tree=True, events=('start', 'end') )
        return stream

    else:
        stream = etree.iterparse( f, huge_tree=False, events=('start', 'end') )
        return stream
