"""
Nordlys API

This is the main console application for the Nordlys API

@author Krisztian Balog
@author Faegheh Hasibi
@author Shuo Zhang
"""
from flask import Flask, jsonify, request
from nordlys.config import MONGO_ENTITY_COLLECTIONS, ELASTIC_INDICES
from nordlys.logic.entity.entity import Entity
from nordlys.services.el import EL
from nordlys.services.er import ER
from nordlys.services.tti import TTI

# variables
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
    return "This is the Nordlys API."


@app.route("/catalog/<collection>/<enxtity_id>")
def catalog(collection, entity_id):
    if collection not in MONGO_ENTITY_COLLECTIONS:
        return error("collection does not exist.")
    entity = __entity.lookup_en(entity_id)
    if entity is None:
        return error("entity_id does not exist.")
    return jsonify(**entity)


# /el/<index>?q=xx[&start=xx&field=xx&model=xx&smoothing_method=xx&smoothing_param=xx]
@app.route("/er/<index>")
def retrieval(index):
    if index not in ELASTIC_INDICES:
        return error("Index does not exist!")
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")

    config = {
        "index_name": index,
        "first_pass": {
            "fields_return": request.args.get("fields_return", None),
            "num_docs": request.args.get("1st_num_docs", None),
        },
        "start": request.args.get("start", 0),
        "num_docs": request.args.get("num_docs", 100),
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
    print(res)
    return jsonify(**res)


@app.route("/types")
def entity_types():
    query = request.args.get("q", None)
    if query is None:
        return error("Query is not specified.")

    config = dict()
    for param in ["method", "num_docs", "start", "model", "index", "ec_k_cutoff", "field", "smoothing_method",
                  "smoothing_param"]:
        if request.args.get(param, None) is not None:
            config[param] = request.args.get(param)
    tti = TTI(config)
    res = tti.identify(query)
    return jsonify(**res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
