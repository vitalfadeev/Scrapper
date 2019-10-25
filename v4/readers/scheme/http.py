import io
import requests
from requests.adapters import HTTPAdapter

MAX_RETRIES = 5
_cache = {}


def _get_with_retries( url, stream=False ):
    with requests.Session() as session:
        retry_adapter = HTTPAdapter( max_retries=MAX_RETRIES )
        session.mount( 'http://', retry_adapter )
        session.mount( 'https://', retry_adapter )

        response = session.get( url, stream=stream )

        return response


def Reader( url: str, cache=False, stream=False ):
    if stream:
        response = _get_with_retries( url, stream=stream )
        return response
    else:
        if cache:
            if url in _cache:
                return _cache[ url ]
            else:
                response = _get_with_retries( url, stream=stream )

                _cache[ url ] = response
                return response

        else:
            response = _get_with_retries( url, stream=stream )
            return response

