import os
import unittest
import hashlib
import Scrapper_Downloader


def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def sha1sum(filename):
    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * sha1.block_size), b''):
            sha1.update(chunk)
    return sha1.hexdigest()


class MyTestCase(unittest.TestCase):
    def setUp(self):
        ...


    def test_1_https(self):
        url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-sha1sums.txt"

        res = Scrapper_Downloader.download( url, "/tmp/enwiktionary-latest-sha1sums.txt" )

        self.assertTrue( res )


    def test_2_https(self):
        url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-all-titles.gz"

        #if os.path.isfile( "/tmp/enwiktionary-latest-all-titles.gz" ):
        #    os.remove( "/tmp/enwiktionary-latest-all-titles.gz" )

        res = Scrapper_Downloader.download( url, "/tmp/enwiktionary-latest-all-titles.gz" )

        self.assertTrue( res )

        # read hash
        with open("/tmp/enwiktionary-latest-sha1sums.txt") as f:
            hash_expected = ''

            for line in f.readlines():
                if line.find("-all-titles.gz") != -1:
                    hash_expected = line.split(' ', 1)[0]
                    break

        # calculate hash
        hash = sha1sum( "/tmp/enwiktionary-latest-all-titles.gz" )

        # check
        self.assertEqual( hash, hash_expected )


    def test_3_resume(self):
        import multiprocessing
        import time

        url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-all-titles.gz"

        if os.path.isfile( "/tmp/enwiktionary-latest-all-titles.gz" ):
            os.remove( "/tmp/enwiktionary-latest-all-titles.gz" )

        # download
        def run():
            Scrapper_Downloader.download( url, "/tmp/enwiktionary-latest-all-titles.gz" )

        p = multiprocessing.Process( target=run )
        p.start()
        time.sleep( 3 )

        # terminate
        p.terminate()

        self.assertTrue( os.path.isfile( "/tmp/enwiktionary-latest-all-titles.gz.part" ) )


        # resume
        Scrapper_Downloader.download( url, "/tmp/enwiktionary-latest-all-titles.gz" )

        # read hash
        with open("/tmp/enwiktionary-latest-sha1sums.txt") as f:
            hash_expected = ''

            for line in f.readlines():
                if line.find("-all-titles.gz") != -1:
                    hash_expected = line.split(' ', 1)[0]
                    break

        # calculate hash
        hash = sha1sum( "/tmp/enwiktionary-latest-all-titles.gz" )

        # check
        self.assertEqual( hash, hash_expected )


    def test_4_already_downloaded(self):
        url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-all-titles.gz"

        # download
        res = Scrapper_Downloader.download( url, "/tmp/enwiktionary-latest-all-titles.gz" )

        self.assertTrue( res )


if __name__ == '__main__':
    unittest.main()

