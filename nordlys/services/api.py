"""
Nordlys API
===========

This is the main console application for the Nordlys API.

:Authors: Krisztian Balog, Faegheh Hasibi, Shuo Zhang
"""

from flask import Flask, jsonify, request
from nordlys.config import MONGO_ENTITY_COLLECTIONS, ELASTIC_INDICES
from nordlys.logic.entity.entity import Entity
from nordlys.services.el import EL
from nordlys.services.er import ER
from nordlys.services.tti import TTI

from nordlys.core.utils.logging_utils import RequestHandler
import logging, traceback
from time import strftime
from nordlys.config import LOGGING_PATH, PLOGGER


# Constants
DBPEDIA_INDEX = "nordlys_dbpedia_2015_10"

# Variables
__entity = Entity()
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


@app.route("/ec/lookup_id/<path:entity_id>")
def catalog_lookup_id(entity_id):
    entity = __entity.lookup_en(entity_id)
    if entity is None:
        return error("Entity ID '{}' does not exist".format(entity_id))
    return jsonify(**entity)


@app.route("/ec/lookup_sf/dbpedia/<sf>")
def catalog_lookup_sf_dbpedia(sf):
    ce = __entity.lookup_name_dbpedia(sf)
    if ce is None or len(ce) == 0:
        return error("Surface form '{}' does not exist".format(sf))
    return jsonify(**ce)


@app.route("/ec/lookup_sf/facc/<sf>")
def catalog_lookup_sf_facc(sf):
    ce = __entity.lookup_name_facc(sf)
    if ce is None or len(ce) == 0:
        return error("Surface form '{}' does not exist".format(sf))
    return jsonify(**ce)


@app.route("/ec/freebase2dbpedia/<path:fb_id>")
def catalog_fb2dbp(fb_id):
    dbp_ids = __entity.fb_to_dbp(fb_id)
    if dbp_ids is None:
        return error("Freebase ID '{}' does not exist".format(fb_id))
    res = {"dbpedia_ids": dbp_ids}
    return jsonify(**res)


@app.route("/ec/dbpedia2freebase/<path:dbp_id>")
def catalog_dbp2fb(dbp_id):
    fb_ids = __entity.dbp_to_fb(dbp_id)
    if fb_ids is None:
        return error("DBpedia ID '{}' does not exist".format(dbp_id))
    res = {"freebase_ids": fb_ids}
    return jsonify(**res)


# /er?q=xx[&start=xx&field=xx&model=xx&smoothing_method=xx&smoothing_param=xx]
@app.route("/er")
def retrieval():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")

    config = {
        "index_name": DBPEDIA_INDEX,
        "first_pass": {
            "fields_return": request.args.get("fields_return", None),
            "num_docs": request.args.get("1st_num_docs", None),
        },
        "start": request.args.get("start", 0),
        "num_docs": request.args.get("num_docs", None),
        "model": request.args.get("model", None),
        "field": request.args.get("field", None),
        "fields": request.args.get("fields", None),
        "field_weights": request.args.get("field_weights", None),
        "smoothing_method": request.args.get("smoothing_method", None),
        "smoothing_param": request.args.get("smoothing_param", None),
    }
    er = ER(config)
    res = er.retrieve(query)
    return jsonify(**res)


@app.route("/el")
def entity_linking():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")

    config = {
        "method": request.args.get("method", None),
        "threshold": request.args.get("threshold", 0.1)
    }
    el = EL(config, __entity)
    res = el.link(query)
    PLOGGER.debug(res)
    return jsonify(**res)


@app.route("/tti")
def entity_types():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")

    config = dict()
    for param in ["method", "num_docs", "start", "model", "ec_cutoff", "field", "smoothing_method", "smoothing_param"]:
        if request.args.get(param, None) is not None:
            config[param] = request.args.get(param)
    tti = TTI(config)
    res = tti.identify(query)
    return jsonify(**res)


@app.after_request
def after_request(response):
    timestamp = strftime("[%Y-%m-%d %H:%M:%S]")
    logger.info('%s %s %s %s %s %s',
                timestamp, request.remote_addr, request.method,
                request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = strftime("[%Y-%m-%d %H:%M:%S]")
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 timestamp, request.remote_addr, request.method,
                 request.scheme, request.full_path, tb)
    return e.status_code


if __name__ == "__main__":
    handler = RequestHandler(LOGGING_PATH)
    logger = logging.getLogger('nordlys.requests')
    logger.addHandler(handler.fh)
    logger.setLevel(logging.DEBUG)
    app.run(host="127.0.0.1")
