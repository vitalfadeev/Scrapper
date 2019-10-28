from lxml import etree

# XmlStreamReader(xml_stream)

def Reader( f, url, stream=False, tag=None ):
    iter = etree.iterparse( f, huge_tree=False, events=('start', 'end'), tag=tag )
    return iter

