"""
nordlys_app
-----------

Web Interface main module.

@author: Dario Garigliotti
@author: Shuo Zhang
@author: Heng Ding
"""

from requests import ConnectionError, Timeout, get as requests_get
from json import loads as j_loads
from urllib.parse import quote
from flask import Flask
from flask import render_template, request

from www.service_utils import *
from nordlys.config import (ELASTIC_HOSTS, API_HOST, API_PORT, WWW_PORT, WWW_DOMAIN, WWW_SETTINGS,
                            MONGO_ENTITY_COLLECTIONS)

# ----------
# ----------
# Constants

# ----------
# Web interface

# Logics
REQUEST_TIMEOUT = 30  # 0.06  # in seconds
NUM_RESULTS = 10  # Per page, for pagination of ER results
WWW_PAGINATION_MAX_RESULTS_ER = WWW_SETTINGS.get('pagination_max_results_ER', 100)
WWW_PAGINATION_MAX_RESULTS_TTI = WWW_SETTINGS.get('pagination_max_results_TTI', 10)

# ----------
# Nordlys API

PROTOCOL = "http:/"

# Hostnames
SERVER_HOSTNAME_API = "{}:{}".format(API_HOST, API_PORT)
SERVER_HOSTNAME_ELASTIC = ELASTIC_HOSTS[0] if len(ELASTIC_HOSTS) > 0 else "152.94.1.85:9200"


# ----------
# ----------
# Functions

# ----------
# API request layer

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

    url = "/".join([PROTOCOL, SERVER_HOSTNAME_API, service_label])
    if service_label == SERVICE_E_RETRIEVAL:
        url += "?q={}&model={}&start={}&1st_num_docs={}&fields_return={}".format(
            quote(params.get("q", "")),
            params.get("model", "lm"),
            params.get("start", 0),
            params.get("1st_num_docs", 100),
            params.get("fields_return", "abstract"),
        )
        url += "&num_docs={}".format(params.get("num_docs", NUM_RESULTS))

    elif service_label == SERVICE_E_LINKING:
        url += "?q={}".format(quote(params.get("q", "")))

    elif service_label == SERVICE_TTI:
        url += "?q={}&method={}&num_docs={}&start={}&index={}&field={}".format(
            quote(params.get("q", "")),
            params.get("method", "tc"),
            params.get("num_docs", NUM_RESULTS),
            params.get("start", 0),
            params.get("index", TTI_INDEX_FALLBACK_2015_10),
            params.get("field", "_id")
        )
    try:
        print("Service request' URL: {}".format(url))
        r = requests_get(url, timeout=REQUEST_TIMEOUT)
        print(r)
        results = j_loads(r.text)
        total = results.get("total_hits", 0)

        # Obtain postprocessed results to render, if needed
        entity_collection = MONGO_ENTITY_COLLECTIONS[0] if len(MONGO_ENTITY_COLLECTIONS) > 0 else "dbpedia-2015-10"
        results = process_results(results, service_label, protocol=PROTOCOL, server_hostname_api=SERVER_HOSTNAME_API,
                                  entity_collection=entity_collection, request_timeout=REQUEST_TIMEOUT)

    except ConnectionError:
        msg = "We're so sorry. There was a connection error :("
    except Timeout:
        msg = "Timeout while trying to connect to the remote server, or while receiving data from it :("

    return results, total, msg


# -----------------
# Main Web Service entry point

# Initialization and configuration
app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Setting the different routes
# -----------------
# Root
@app.route('/')
def index():
    """Provides the required root app as a template rendering manager"""
    return render_template('index.html', services=init_services(), placeholder="Search for...", domain=WWW_DOMAIN)


# -----------------
# ER service
@app.route('/er', methods=['GET'])
def service_ER():
    """Provides the required ER service as a template rendering manager."""

    # Fall-back init, if the service is run for an empty query
    rendered = render_template('index.html', services=init_services(), placeholder="Search for...", domain=WWW_DOMAIN)

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
                                       service=init_service(service_label, index_name=index_name), domain=WWW_DOMAIN)
        except AssertionError:  # results is None, i.e. there was an error during request
            rendered = render_template("error.html", error_msg=msg, placeholder="Search for...", domain=WWW_DOMAIN)

    return rendered


# -----------------
# EL service
@app.route('/el', methods=['GET'])
def service_EL():
    """Provides the required EL service as a template rendering manager."""

    # Fall-back init, if the service is run for an empty query
    rendered = render_template('index.html', services=init_services(), placeholder="Search for...", domain=WWW_DOMAIN)

    query = request.args.get("query", "")
    if len(query) > 0:
        service_label = SERVICE_E_LINKING

        params = {"q": query}
        results, total, msg = __api_request(service_label, params)

        # Template rendering
        try:
            assert (results is not None)
            rendered = render_template("results_EL.html", query=query, results=results,  # TODO more context params?
                                       service=init_service(service_label), domain=WWW_DOMAIN)
        except AssertionError:  # results is None, i.e. there was an error during request
            rendered = render_template("error.html", error_msg=msg, placeholder="Search for...", domain=WWW_DOMAIN)

    return rendered


# -----------------
# TTI service
@app.route('/tti', methods=['GET'])
def service_TTI():
    """Provides the required TTI service as a template rendering manager."""

    # Fall-back init, if the service is run for an empty query
    rendered = render_template('index.html', services=init_services(), placeholder="Search for...", domain=WWW_DOMAIN)

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
                                       service=init_service(service_label, index_name=index_name), domain=WWW_DOMAIN)
        except AssertionError:  # results is None, i.e. there was an error during request
            rendered = render_template("error.html", error_msg=msg, placeholder="Search for...", domain=WWW_DOMAIN)

    return rendered


# -------------
# Main script

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=WWW_PORT)
