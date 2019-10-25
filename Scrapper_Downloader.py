"""
Download file.

.. figure:: ../_static/img/downloader.png

Designed for downloading large files (600 M ~ 36 G).

Support:

- resume downloading
- 5 retries when link broken
- show progress bar

::

    from Scrapper_Downloader import download
    url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2"
    dest = "./cached/enwiktionary-latest-pages-articles.xml.bz2"
    download( url, dest )

"""

import sys
import os
import os.path
import requests
import urllib3
import logging
from requests.adapters import HTTPAdapter

log = logging.getLogger(__name__)
DOWNLOAD_TIMEOUT = 33   # maximum time to connect and fetch data block
DOWNLOAD_RETRY = 5      # maximum retries attempts to connect and download file


def requests_retry_session( retries=5 ):
    """
    Helper function. It help retry download when link broken. `retries` retries.

    Args:
        retries (int):  Maximum retries attempts to connect and download file

    Returns (request.Session):
        Session object

    ::

        session = requests_retry_session( retries=5 )
        response = session.get( url )

    """
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_http_file_size( url ):
    """
    Get size of remote file `url`

    Args:
        url (str): Remote file name

    Returns:
        (int) file size

    ::

        url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2"
        remote_file_size = get_http_file_size( url )

    """
    session = requests_retry_session( retries=DOWNLOAD_RETRY )
    response = session.get(url, stream=True, verify=False, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT)
    size = response.headers['Content-length']
    response.close()
    return int(size)


def get_local_file_size( file_name ):
    """
    Return size of local file `file_name`

    Args:
        file_name (str):  Path to file

    Returns:
        (int) file size


    ::

        local_file = "./cached/enwiktionary-latest-pages-articles.xml.bz2"
        local_file_size = get_local_file_size( local_file )

    """
    return os.path.getsize(file_name)


def _download_with_progress( response, f, remote_file_size, file_name, resume_byte_pos ):
    """
    Download and show progress bar.

    It internal function.

    It read chunks from stream  `response` and save to the file `f`.

    It show progress bar each 1 M.

    Args:
        r (request stream object):
        f (file object:
        remote_file_size (int):
        file_name (str):
        resume_byte_pos (int):

    """
    readed = resume_byte_pos
    response.raw.decode_content = False
    readeed_pos = readed % (1024 * 1024)

    # download
    for chunk in response:
        f.write( chunk )

        readed += len( chunk )

        # progress bar
        if int(readed / 1024 / 1024) != readeed_pos:
            PROGRESS_BAR_WIDTH = 40

            fill_size = int( round( PROGRESS_BAR_WIDTH * readed / remote_file_size, 0 ) )
            rest_size = PROGRESS_BAR_WIDTH - fill_size

            fill_bar = '#' * fill_size
            rest_bar = '-' * rest_size

            bar = fill_bar + rest_bar

            print( "\r Download progress: [{}] {} M / {} M" \
                   .format(
                        bar,
                        int(readed / 1024 / 1024),
                        int(remote_file_size / 1024 / 1024)
                    ),
                    end="", flush=True
            )
            readeed_pos = int(readed / 1024 / 1024)

    print()


def _continue_downloading(url, local_file, remote_file_size, resume_byte_pos=0):
    """
    Continue download `url` to `local_file`

    It function for internal use.

    It compare sizes: remote and local. And download file if need. Or resume downloading.

    It retry `DOWNLOAD_RETRY` times when link broken.

    It wait `DOWNLOAD_TIMEOUT` for connection and retrieve data.

    Args:
        url (str):                  Remote file url
        local_file (str):           Local file path and name
        remote_file_size (int):     Remote file size
        resume_byte_pos (int):      Resume from this position. Also it mean local file size.

    """
    file_name = os.path.basename( local_file )

    if resume_byte_pos == 0:
        # new file
        session = requests_retry_session( retries=DOWNLOAD_RETRY )
        response = session.get(url, stream=True, verify=False, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT)

        with open(local_file, 'wb') as f:
            _download_with_progress( response, f, remote_file_size, file_name, resume_byte_pos )

        response.close()

    else:
        # append
        resume_header = { 'Range': 'bytes=%d-' % resume_byte_pos }
        session = requests_retry_session( retries=DOWNLOAD_RETRY )
        response = session.get(url, stream=True, verify=False, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT,
                         headers=resume_header)

        with open(local_file, 'ab') as f:
            f.truncate( resume_byte_pos )
            _download_with_progress( response, f, remote_file_size, file_name, resume_byte_pos )

        response.close()


def _download_with_resume(url, local_file):
    """
    Download `url` to `local_file`.

    It internal function.

    It create local file with '.part' at end. When download finished successfully '.part' will removed.

    It can resume downloading. It get file size of remote file. Compare with local file size. And download rest.

    Args:
        url (str):          Remote file url
        local_file (str):   Local file path and name

    Returns:
        `True` if downloaded
        `None` else
    """
    # check already downloaded
    if os.path.isfile(local_file):
        return True

    # check part file
    part_file = local_file + ".part"

    if os.path.isfile(part_file): # file exists
        # check size
        local = get_local_file_size(part_file)
        remote = get_http_file_size(url)

        if local == remote:
            return True  # OK
        else:
            # continue downloading
            resume_pos = local - 4096   # delete 4096 Bytes tail. for remove '500 ... error message'
            if resume_pos < 0:
                resume_pos = 0

            _continue_downloading( url, part_file, remote, resume_pos )

    else: # no local file
        # downloading
        remote = get_http_file_size(url)   # for progress bar
        _continue_downloading( url, part_file, remote, 0 )

    # rename part_file to local_file
    local = get_local_file_size(part_file)
    if local == remote:
        os.rename(part_file, local_file)


def download( url, local_file, attempts=5 ):
    """
    Download file from `url` to `local_file`.

    Args:
        url (str):          Remote file url
        local_file (str):   Local file path and name
        attempts (int):     When link is broken retry `attempts` times

    Returns:
        `True` if downloading finished.
        `None` else.

    ::

        from Scrapper_Downloader import download
        url = "https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2"
        dest = "./cached/enwiktionary-latest-pages-articles.xml.bz2"
        download( url, dest )

    """
    log.debug( "download: %s", url )
    for i in range( attempts ):
        try:
            _download_with_resume( url, local_file )
            return  True

        except requests.exceptions.ConnectionError as e:
            pass

        except urllib3.exceptions.ReadTimeoutError as e:
            pass
