"""
config
------

Global nordlys config.

:Author: Krisztian Balog
:Author: Faegheh Hasibi
"""
import logging
import os
from nordlys.core.utils.file_utils import FileUtils
from nordlys.core.utils.logging_utils import PrintHandler


def load_nordlys_config(file_name):
    """Loads nordlys config file. If local file is provided, global one is ignored."""
    config_path = os.sep.join([BASE_DIR, "config"])
    local_config = os.sep.join([config_path, "local", file_name])
    if os.path.exists(local_config):
        return FileUtils.load_config(local_config)
    else:
        return FileUtils.load_config(os.sep.join([config_path, file_name]))


# global variable for entity linking
KB_SNAPSHOT = None

# Nordlys DIRs
NORDLYS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.sep.join([BASE_DIR, "data"])
LIB_DIR = os.sep.join([BASE_DIR, "lib"])


# config for MongoDB
MONGO_CONFIG = load_nordlys_config("mongo.json")
MONGO_HOST = MONGO_CONFIG["host"]
MONGO_DB = MONGO_CONFIG["db"]
MONGO_COLLECTION_DBPEDIA = MONGO_CONFIG["collection_dbpedia"]
MONGO_COLLECTION_SF_FACC = MONGO_CONFIG["collection_sf_facc"]
MONGO_COLLECTION_SF_DBPEDIA = MONGO_CONFIG["collection_sf_dbpedia"]
MONGO_COLLECTION_WORD2VEC = MONGO_CONFIG["collection_word2vec"]
MONGO_COLLECTION_FREEBASE2DBPEDIA = MONGO_CONFIG["collection_freebase2dbpedia"]
MONGO_ENTITY_COLLECTIONS = MONGO_CONFIG["entity_collections"]

# config for Elasticsearch
ELASTIC_CONFIG = load_nordlys_config("elastic.json")
ELASTIC_HOSTS = ELASTIC_CONFIG["hosts"]
ELASTIC_SETTINGS = ELASTIC_CONFIG["settings"]
ELASTIC_INDICES = ELASTIC_CONFIG["indices"]
ELASTIC_TTI_INDICES = ELASTIC_CONFIG["tti_indices"]

# config for trec_eval
TREC_EVAL = os.sep.join([LIB_DIR, "trec_eval", "trec_eval"])

# config for API
API_CONFIG = load_nordlys_config("api.json")
API_HOST = API_CONFIG["host"]
API_PORT = int(API_CONFIG["port"])

# config for Web interface
WWW_CONFIG = load_nordlys_config("www.json")
WWW_HOST = WWW_CONFIG["host"]
WWW_PORT = int(WWW_CONFIG["port"])
WWW_DOMAIN = WWW_CONFIG["domain"]
WWW_SETTINGS = WWW_CONFIG["settings"]

# config for RequestLogger
LOGGING_PATH = os.sep.join([BASE_DIR, "logs"])
# config for PrintLogger (PLOGGER)
LOGGING_LEVEL = logging.INFO
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)
PLOGGER = logging.getLogger("nordlys")
PLOGGER.addHandler(PrintHandler(LOGGING_LEVEL).ch)
PLOGGER.setLevel(LOGGING_LEVEL)
PLOGGER.propagate = 0