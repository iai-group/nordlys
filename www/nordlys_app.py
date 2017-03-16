"""
app
---

Web Interface main module.

@author: Dario Garigliotti
@author: Shuo Zhang
@author: Heng Ding
"""

from requests import ConnectionError, Timeout, get as requests_get
from json import loads as j_loads
from urllib.parse import quote  # , quote_plus, unquote_plus
from operator import itemgetter
from flask import Flask
from flask import render_template, request

from www.service_utils import *
from nordlys.config import ELASTIC_HOSTS, API_HOST, API_PORT, WWW_PORT, WWW_SETTINGS

# ----------
# ----------
# Constants

# ----------
# Web interface

# Logics
REQUEST_TIMEOUT = 60  # 0.06  # in seconds
NUM_RESULTS = 10  # Per page, for pagination of ER results
WWW_PAGINATION_MAX_RESULTS_ER = WWW_SETTINGS.get('pagination_max_results_ER', 1000)
WWW_PAGINATION_MAX_RESULTS_TTI = WWW_SETTINGS.get('pagination_max_results_TTI', 10)

# ----------
# Nordlys API

PROTOCOL = "http:/"
# ---
# Load it from API constants from nordlys.config
# Server host:port...

# SERVER_HOSTNAME_API = "localhost:8080"  # API

SERVER_HOSTNAME_API = "{}:{}".format(API_HOST, API_PORT)  # == "152.94.1.85:5000"  # API
SERVER_HOSTNAME_ELASTIC = ELASTIC_HOSTS[0] if len(ELASTIC_HOSTS) > 0 else "152.94.1.85:9200"  # Elastic


# SERVER_HOSTNAME = "localhost:8080"  # same port as specified in tunneling step if that's the case


# ---

# ----------
# ----------
# Functions

# ----------
# API wrapper

# def __api_request(index_name, params, service_label):
#     """Wraps the access to the Nordlys API. It returns a 3-uple (results, total no. of results, pretty status message).
# 
#     :param index_name: name of index.
#     :param params: request params.
#     :param service_label: a constant for the required service_label.
#     :return: a list of docIDs.
#     """
#     results = None  # default init, it remainss None if request returns error
#     total = 0
#     msg = ""
# 
#     url = "/".join([PROTOCOL, SERVER_HOSTNAME_ELASTIC, index_name, "_search"])
# 
#     try:
#         r = requests_get(url, params, timeout=REQUEST_TIMEOUT)  # TODO AJAXify this?
#         res = j_loads(r.text)
#         results = [r for r in res.get("hits", {}).get("hits", {})]
#         total = res.get("hits", {}).get("total", 0)
# 
#         # Obtain postprocessed results to render, if needed
#         results = process_results(results, service_label)
#     except ConnectionError:
#         msg = "We're so sorry. There was a connection error :("
#     except Timeout:
#         msg = "Timeout while trying to connect to the remote server, or while receiving data from it :("
# 
#     return results, total, msg


def __api_request(service_label, params, index_name=None):
    """Wraps the access to the Nordlys API. It returns a 3-uple (results, total no. of results, pretty status message).

    :param service_label: a constant for the required service_label.
    :param params: request params.
    :param index_name: optional; name of index.
    :return: a list of docIDs.
    """
    results = None  # default init, it remains None if request returns error
    total = 0
    msg = ""

    url = ""
    if service_label == SERVICE_E_RETRIEVAL:
        url = "/".join([PROTOCOL, SERVER_HOSTNAME_API, "er", index_name])
        url += "?q={}&model={}&start={}&1st_num_docs={}&fields_return={}".format(
            quote(params.get("q", "")),
            params.get("model", "lm"),
            params.get("start", 0),
            params.get("1st_num_docs", 100),
            params.get("fields_return", "abstract"),
        )
        url += "&num_docs={}".format(params.get("num_docs", NUM_RESULTS))

    if service_label == SERVICE_E_LINKING:
        url = "/".join([PROTOCOL, SERVER_HOSTNAME_API, "el"])
        url += "?q={}".format(quote(params.get("q", "")))

    elif service_label == SERVICE_TTI:

        # TODO ideal with API

        url = "/".join([PROTOCOL, SERVER_HOSTNAME_API, "types"])
        url += "?q={}&method={}&num_docs={}&start={}&index={}&field={}".format(
            quote(params.get("q", "")),
            params.get("method", "tc"),
            params.get("num_docs", NUM_RESULTS),
            params.get("start", 0),
            params.get("index", TTI_INDEX_FALLBACK_2015_10),
            params.get("field", "_id")
        )

        # TODO working on local after tunneling Elastic

        # url = "/".join([PROTOCOL, "localhost:8080", index_name, "_search?q={}&fields=_id".format(
        #     quote(params.get("q", "")))])

        # TODO working on gustav1 directly to Elastic
        # url = "/".join([PROTOCOL, SERVER_HOSTNAME_ELASTIC, index_name, "_search?q={}&fields=_id".format(
        #     quote(params.get("q", "")))])

    try:
        print(url)
        r = requests_get(url, timeout=REQUEST_TIMEOUT)  # TODO AJAXify this?
        results = j_loads(r.text)
        # total = WWW_PAGINATION_MAX_RESULTS_ER
        total = len(results.get("results", 0))

        # Obtain postprocessed results to render, if needed
        results = process_results(results, service_label)

    except ConnectionError:
        msg = "We're so sorry. There was a connection error :("
    except Timeout:
        msg = "Timeout while trying to connect to the remote server, or while receiving data from it :("

    return results, total, msg


# -------------
# Other auxiliary functions
# ...

# -----------------
# Main Web Service entry point

# Initialization and configuration
app = Flask(__name__)


# Setting the different routes
# @app.route('/')
# def index():
#     return render_template('index.html')
#
@app.route('/')
def index():
    """Provides the required root app as a template rendering manager"""
    return render_template('index.html', services=init_services(), query="Search for...")


# -----------------
# ER service
@app.route('/service/er', methods=['GET'])
def service_ER():
    """Provides the required ER service as a template rendering manager."""

    # Fall-back init, if the service is run for an empty query
    rendered = render_template('index.html', services=init_services(), query="Search for...")

    query = request.args.get("query", "")
    if len(query) > 0:
        service_label = SERVICE_E_RETRIEVAL

        # Collection
        index_name = request.args.get("collection", ER_INDEX_FALLBACK_2015_10)

        # Requesting results
        page = int(request.args.get("page", 0))
        params = {
            "q": query,
            "model": "lm",
            "start": page * NUM_RESULTS,
            # "fields": ["_id", "_source"],
            "fields_return": "abstract",
            "1st_num_docs": 100
        }
        results, total, msg = __api_request(service_label, params, index_name)

        # Pagination
        pagination = {}  # Contextual data for handling pagination in the template
        pagination_total = min(total, WWW_PAGINATION_MAX_RESULTS_ER)
        pagination["results_total_to_show"] = (str(pagination_total)
                                               if total <= WWW_PAGINATION_MAX_RESULTS_ER
                                               else "{}+".format(WWW_PAGINATION_MAX_RESULTS_ER))
        pagination["results_from"] = page * NUM_RESULTS + 1
        results_to = (page + 1) * NUM_RESULTS
        pagination["results_to"] = results_to if results_to <= pagination_total else pagination_total
        pagination["current_page"] = page
        pagination["results_pages"] = {
            "first": 0,
            "previous": page - 1,
            "next": page + 1,
            # if we set: "last": int(pagination_total / NUM_RESULTS)
            # then when pagination_total is multiple of NUM_RESULTS, last is wrongly 1 ahead the right last. So:
            "last": int((pagination_total - 1) / NUM_RESULTS)
        }

        # Template rendering
        try:
            assert (results is not None)
            rendered = render_template("results_ER.html", query=query, results=results, pagination=pagination,
                                       human_readable_collection=INDEX_2_HUMAN_LABEL.get(index_name, index_name),
                                       service=init_service(service_label, index_name=index_name))
        except AssertionError:  # results is None, i.e. there was an error during request
            rendered = render_template("error.html", error_msg=msg)

    return rendered


# -----------------
# EL service
@app.route('/service/el', methods=['GET'])
def service_EL():
    """Provides the required EL service as a template rendering manager."""

    # Fall-back init, if the service is run for an empty query
    rendered = render_template('index.html', services=init_services(), query="Search for...")

    query = request.args.get("query", "")
    if len(query) > 0:
        service_label = SERVICE_E_LINKING

        # -------
        # TODO
        #
        # Collection?
        # index_name = None

        # Requesting results
        # results, msg = __api_request(index_name, query, service)

        params = {
            "q": query,
        }
        results, total, msg = __api_request(service_label, params)

        # -------

        # Template rendering
        try:
            assert (results is not None)
            rendered = render_template("results_EL.html", query=query, results=results,  # TODO more context params?
                                       service=init_service(service_label))
        except AssertionError:  # results is None, i.e. there was an error during request
            rendered = render_template("error.html", error_msg=msg)

    return rendered


# -----------------
# TTI service
@app.route('/service/tti', methods=['GET'])
def service_TTI():
    """Provides the required TTI service as a template rendering manager."""

    # Fall-back init, if the service is run for an empty query
    rendered = render_template('index.html', services=init_services(), query="Search for...")

    query = request.args.get("query", "")
    if len(query) > 0:
        service_label = SERVICE_TTI

        # Collection
        index_name = request.args.get("collection", TTI_INDEX_FALLBACK_2015_10)

        # Requesting results
        page = int(request.args.get("page", 0))

        params = {
            "q": query,
            "method": "tc",
            "index": TTI_INDEX_FALLBACK_2015_10,
            "num_docs": 10,
            "start": page * NUM_RESULTS,
            "field": "_id"  # NOTE: important NOT to get full doc from type-centric indices!
        }
        results, total, msg = __api_request(service_label, params, index_name)

        # Template rendering
        try:
            assert (results is not None)
            rendered = render_template("results_TTI.html", query=query, results=results,
                                       human_readable_collection=INDEX_2_HUMAN_LABEL.get(index_name, index_name),
                                       service=init_service(service_label, index_name=index_name))
        except AssertionError:  # results is None, i.e. there was an error during request
            rendered = render_template("error.html", error_msg=msg)

    return rendered


# -------------
# Main script

if __name__ == '__main__':
    # app.run(debug=True, port=WWW_PORT)  # TODO working on local
    app.run(host="0.0.0.0", port=WWW_PORT)
