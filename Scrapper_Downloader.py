import sys
import os
import os.path
import requests
import urllib3
import logging

log = logging.getLogger(__name__)
DOWNLOAD_TIMEOUT = 33


def get_http_file_size(url):
    r = requests.get(url, stream=True, verify=False, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT)
    size = r.headers['Content-length']
    r.close()
    return int(size)


def get_local_file_size(file_name):
    return os.path.getsize(file_name)


def _download_with_progress(r, f, remote_file_size, file_name, resume_byte_pos):
    readed = resume_byte_pos
    r.raw.decode_content = False
    readeed_pos = readed % (1024 * 1024)

    print()

    for chunk in r:
        f.write( chunk )

        readed += len( chunk )

        if int(readed / 1024 / 1024) != readeed_pos:
            print( "\r Download progress: {} M / {} M" \
                   .format(
                        int(readed / 1024 / 1024),
                        int(remote_file_size / 1024 / 1024)
                    ),
                    end="", flush=True
            )
            readeed_pos = int(readed / 1024 / 1024)

    print()


def continue_downloading(url, local_file, remote_file_size, resume_byte_pos=0):
    file_name = os.path.basename( local_file )

    if resume_byte_pos == 0:
        # new file
        r = requests.get(url, stream=True, verify=False, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT)

        with open(local_file, 'wb') as f:
            _download_with_progress(r, f, remote_file_size, file_name, resume_byte_pos)

        r.close()

    else:
        # append
        resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
        r = requests.get(url, stream=True, verify=False, allow_redirects=True, timeout=DOWNLOAD_TIMEOUT,
                         headers=resume_header)

        with open(local_file, 'ab') as f:
            _download_with_progress(r, f, remote_file_size, file_name, resume_byte_pos)

        r.close()


def _download_with_resume(url, local_file):
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
            continue_downloading( url, part_file, remote, local )

    else: # no local file
        # downloading
        remote = get_http_file_size(url)
        continue_downloading( url, part_file, remote, 0 )

    # rename part_file to local_file
    local = get_local_file_size(part_file)
    if local == remote:
        os.rename(part_file, local_file)


def download_with_resume(url, local_file, attempts=5):
    log.debug( "download: %s", url )
    for i in range(attempts):
        try:
            _download_with_resume(url, local_file)
            return  True

        except requests.exceptions.ConnectionError as e:
            pass

        except urllib3.exceptions.ReadTimeoutError as e:
            pass
