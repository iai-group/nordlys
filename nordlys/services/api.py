"""
Nordlys API
===========

This is the main console application for the Nordlys API.

:Authors: Krisztian Balog, Faegheh Hasibi, Shuo Zhang, Fadwa Maatug
"""

from flask import Flask, jsonify, request
import threading

from nordlys.core.retrieval.elastic_cache import ElasticCache
from nordlys.logic.entity.entity import Entity
from nordlys.logic.features.feature_cache import FeatureCache
from nordlys.services.el import EL
from nordlys.services.er import ER
from nordlys.services.tti import TTI

from nordlys.core.utils.logging_utils import RequestHandler
from nordlys.core.utils.Api_handler import API_Handler
import logging, traceback
from time import strftime
from nordlys.config import LOGGING_PATH, PLOGGER, ELASTIC_INDICES, Api_Log_Path

# Variables
DBPEDIA_INDEX = ELASTIC_INDICES[0]
__entity = Entity()
__elastic = ElasticCache(DBPEDIA_INDEX)
__fcache = FeatureCache()
app = Flask(__name__)


def error(str):
    """
    @todo complete error handling

    :param str:
    :return:
    """
    res = {"ERROR": str}
    return jsonify(**res)


@app.route("/")
def index():
    return "This is the Nordlys API"


# /ec/lookup_id?entity_id=xxx&key=yyy
@app.route("/ec/lookup_id")
def catalog_lookup_id():
    entity_id = request.args.get("entity_id", None)
    if entity_id is None:
        return error("Entity Id is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    entity = __entity.lookup_en(entity_id)
    if entity is None:
        return error("Entity ID '{}' does not exist".format(entity_id))
    return jsonify(**entity)


# /ec/lookup_sf/dbpedia?sf=xxx&key=yyy
@app.route("/ec/lookup_sf/dbpedia")
def catalog_lookup_sf_dbpedia():
    sf = request.args.get("sf", None)
    if sf is None:
        return error("Surface form is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    ce = __entity.lookup_name_dbpedia(sf)
    if ce is None or len(ce) == 0:
        return error("Surface form '{}' does not exist".format(sf))
    return jsonify(**ce)


# /ec/lookup_sf/facc?sf=xxx&key=yyy
@app.route("/ec/lookup_sf/facc")
def catalog_lookup_sf_facc():
    sf = request.args.get("sf", None)
    if sf is None:
        return error("Surface form is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    ce = __entity.lookup_name_facc(sf)
    if ce is None or len(ce) == 0:
        return error("Surface form '{}' does not exist".format(sf))
    return jsonify(**ce)


# /ec/freebase2dbpedia?fb_id=xxx&key=yyy
@app.route("/ec/freebase2dbpedia")
def catalog_fb2dbp():
    fb_id = request.args.get("fb_id", None)
    if sf is None:
        return error("Freebase ID is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    dbp_ids = __entity.fb_to_dbp(fb_id)
    if dbp_ids is None:
        return error("Freebase ID '{}' does not exist".format(fb_id))
    res = {"dbpedia_ids": dbp_ids}
    return jsonify(**res)


# /ec/dbpedia2freebase?dbp_id=xxx&key=yyy
@app.route("/ec/dbpedia2freebase")
def catalog_dbp2fb():
    dbp_id = request.args.get("dbp_id", None)
    if sf is None:
        return error("DBpedia ID is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    fb_ids = __entity.dbp_to_fb(dbp_id)
    if fb_ids is None:
        return error("DBpedia ID '{}' does not exist".format(dbp_id))
    res = {"freebase_ids": fb_ids}
    return jsonify(**res)


# /er?q=xx[&start=xx&field=xx&model=xx&smoothing_method=xx&smoothing_param=xx]&key=xxx
@app.route("/er")
def retrieval():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    config = {"first_pass": {}}
    for param in ["fields_return", "1st_num_docs"]:
        if request.args.get(param, None) is not None:
            config["first_pass"][param] = request.args.get(param)
    for param in ["index_name", "start", "num_docs", "model", "fields", "smoothing_method", "smoothing_param"]:
        if request.args.get(param, None) is not None:
            config[param] = request.args.get(param)
    er = ER(config, __elastic)
    res = er.retrieve(query)
    return jsonify(**res)


@app.route("/el")
def entity_linking():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    config = {
        "method": request.args.get("method", None),
        "threshold": request.args.get("threshold", 0.1)
    }
    el = EL(config, __entity, __elastic, __fcache)
    res = el.link(query)
    # PLOGGER.debug(res)
    return jsonify(**res)


@app.route("/tti")
def entity_types():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")
    api_key = request.args.get("key", None)
    ip_address = request.remote_addr
    msg = api_handler.func_handler(api_key, ip_address)
    if msg is not True:
        return error(msg)
    config = dict()
    params = ["method", "num_docs", "start", "model", "ec_cutoff", "field", "smoothing_method", "smoothing_param"]
    for param in params:
        if request.args.get(param, None) is not None:
            config[param] = request.args.get(param)
    tti = TTI(config)
    res = tti.identify(query)
    return jsonify(**res)


@app.after_request
def after_request(response):
    timestamp = strftime("[%Y-%m-%d %H:%M:%S]")
    logger.info('%s %s %s %s %s', request.remote_addr, request.method, request.path, response.status,
                request.full_path.split("?")[1])
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime("[%Y-%m-%d %H:%M:%S]")
    logger.error('%s %s %s %s %s %s', request.remote_addr, request.method, request.path, e.status_code, "Error",
                 request.full_path.split("?")[1])
    return e.status_code


def worker(event, sleep):
    while True:
        try:
            event.wait(sleep)
            api_handler.update_api_file()  # update the API key-quota file
        except KeyboardInterrupt:
            break


def update(sleep):
    event = threading.Event()
    thread = threading.Thread(target=worker, args=(event, sleep,), daemon=True)
    thread.start()


if __name__ == "__main__":
    api_handler = API_Handler(Api_Log_Path, limit=1000)
    handler = RequestHandler(LOGGING_PATH)
    logger = logging.getLogger('nordlys.requests')
    logger.addHandler(handler.fh)
    logger.setLevel(logging.DEBUG)
    update(60 * 20)  # update the API key-quota file every 20 minutes
    app.run(host="0.0.0.0")
