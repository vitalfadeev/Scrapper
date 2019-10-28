local_file = "../cached/dewiki-latest-pages-articles.xml.bz2.part"
resume_byte_pos = 1024

with open( local_file, 'ab' ) as f:
    f.truncate( resume_byte_pos )
