from . import Scrapper_Wiktionary
from wiktionary.en import Scrapper_Wiktionary_EN

import os
import logging
import logging.config

if os.path.isfile('logging.ini'):
    logging.config.fileConfig('logging.ini')
