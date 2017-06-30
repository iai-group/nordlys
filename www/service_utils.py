"""Web Interface service utilities.

service_utils
--------------

:Author: Dario Garigliotti
"""

from re import sub as re_sub
from requests import ConnectionError, Timeout, get as requests_get
from json import loads as j_loads
from urllib.parse import quote

from www.entity_card_data import *

# -----------------
# -----------------
#  Constants
# -----------------

# -------
# Services
# NOTE: not only used as constants to distinguish among services here in service_utils module, but their actual strings
# are the same as used in service URLs so we use them for generalizing some templates, e.g. the pagination one.
SERVICE_E_RETRIEVAL = "er"
SERVICE_E_LINKING = "el"
SERVICE_TTI = "tti"

SERVICES_TO_PROVIDE = [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, SERVICE_TTI]

# -------
# Indices
ER_INDEX_FALLBACK_2015_10 = "nordlys_dbpedia_2015_10"
ER_INDEX_TOY = "toy_index"
TTI_INDEX_FALLBACK_2015_10 = "dbpedia_2015_10_types_bm25"
TTI_INDEX_DBPEDIA_3_9 = "dbpedia_3_9_types_bm25"
# -------
# Methods
ER_METHOD_FALLBACK = "elastic"
EL_METHOD_FALLBACK = "cmns"
TTI_METHOD_FALLBACK_TC = "type_centric"
TTI_METHOD_EC = "entity_centric"

# -------
# DBpedia settings
DBPEDIA_HOSTNAME = "http://dbpedia.org"
SERVICE_TO_DBPEDIA_SUBHOST = {SERVICE_E_RETRIEVAL: "page",
                              SERVICE_E_LINKING: "page",
                              SERVICE_TTI: "ontology"}

WIKIPEDIA_HOSTNAME = "https://en.wikipedia.org"
SERVICE_TO_WIKIPEDIA_SUBHOST = {SERVICE_E_RETRIEVAL: "wiki"}

# -------
# Search results fields
RESULT_DOC_TITLE_K = "doc_title"
RESULT_DOC_ID_K = "doc_id"
RESULT_FREEBASE_ID_K = "doc_freebase_id"
RESULT_URL_DBPEDIA_K = "doc_url_dbpedia"
RESULT_URL_WIKIPEDIA_K = "doc_url_wikipedia"
RESULT_DOC_SNIPPET_K = "doc_snippet"
RESULT_DOC_PICTURE_K = "doc_picture"
RESULT_DOC_SCORE_K = "doc_score"
RESULT_LINKED_SUBSTR_K = "linked_substring"
RESULT_EL_TO_SHOW_K = "el_formatted_result_to_show"
RESULT_DOC_CARD_K = "doc_card"
RESULT_DOC_TYPE_K = "doc_type"

# -------
# Human-readable labels
INDEX_2_HUMAN_LABEL = {ER_INDEX_FALLBACK_2015_10: "DBpedia 2015-10",  # ER...
                       ER_INDEX_TOY: "Toy Index :)",
                       TTI_INDEX_FALLBACK_2015_10: "DBpedia 2015-10",  # TTI...
                       TTI_INDEX_DBPEDIA_3_9: "DBpedia 3.9"
                       }

METHOD_2_HUMAN_LABEL = {ER_METHOD_FALLBACK: "Elastic",
                        EL_METHOD_FALLBACK: "Commonness",
                        TTI_METHOD_FALLBACK_TC: "Type-centric"
                        }

# -------
# More auxiliary data
MAX_ABSTRACT_LEN = 500  # in number of characters


# -----------------
# -----------------
#  Classes
# -----------------

# A wrapper class, and then some functionalities
class ServiceWrapper(object):
    """Simple class, wrapping service information."""

    def __init__(self, label, selected_index, other_indices, selected_method, other_methods, default_html_names=False):
        """

        :param label: a service_label label constant in [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, SERVICE_TTI].
        :param selected_index:
        :param other_indices: a tuples list [(index, human-readable index label)] for all the other available indices, \
        EXCEPTING the selected one.
        :param selected_method:
        :param other_methods: a tuples list [(method, human-readable method label)] for all the other available
        methods, EXCEPTING the selected one.
        :param default_html_names:
        :return:
        """
        self.label = label  # e.g. SERVICE_E_RETRIEVAL
        self.selected_index = selected_index
        self.other_indices = other_indices  # all the other available indices, EXCEPTING the selected one
        self.selected_method = selected_method
        self.other_methods = other_methods  # all the other available methods, EXCEPTING the selected one

        if default_html_names:
            if label is SERVICE_E_RETRIEVAL:
                self.button_id = "entityRetrievalButton"
                self.button_name = "entityRetrieval"
                self.button_value = "Entity Retrieval"
                self.select_id_name = "erCollection"
                self.hint_id = "entityRetrievalHint"
                self.hint_inner = ("Click <em>Entity Retrieval</em> to obtain relevant results for your query. "
                                   "Select from the options the index to use.")

            elif label is SERVICE_E_LINKING:
                self.button_id = "entityLinkingButton"
                self.button_name = "entityLinking"
                self.button_value = "Entity Linking"
                self.hint_id = "entityLinkingHint"
                self.hint_inner = "Click <em>Entity Linking</em> to link the entities your query."

            elif label is SERVICE_TTI:
                self.button_id = "ttiButton"
                self.button_name = "tti"
                self.button_value = "Target Type Indentification"
                self.select_id_name = "ttiCollection"
                self.hint_id = "ttiHint"
                self.hint_inner = ("Click <em>Target Type Identification</em> to obtain ranked types for your query. "
                                   "Select from the options the index to use.")


# -----------------
# -----------------
#  Functions
# -----------------


# -----------------
# Common to services

def get_all_indices(service_label):
    """Given a service_label label, returns all the available indices to choose among, and the default one.

    :param service_label: a service_label label constant in [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, \
    SERVICE_TTI].
    :return:
    """
    if service_label is SERVICE_E_RETRIEVAL:
        default_index = (
            ER_INDEX_FALLBACK_2015_10, INDEX_2_HUMAN_LABEL.get(ER_INDEX_FALLBACK_2015_10, "DBpedia 2015-10"))
        other_indices = [(ER_INDEX_TOY, INDEX_2_HUMAN_LABEL.get(ER_INDEX_TOY, "Toy Index :)"))]
    elif service_label is SERVICE_E_LINKING:
        default_index = ("", "Index")
        other_indices = []
    elif service_label is SERVICE_TTI:
        default_index = (
            TTI_INDEX_FALLBACK_2015_10, INDEX_2_HUMAN_LABEL.get(TTI_INDEX_FALLBACK_2015_10, "DBpedia 2015-10"))
        other_indices = [(TTI_INDEX_DBPEDIA_3_9, INDEX_2_HUMAN_LABEL.get(TTI_INDEX_DBPEDIA_3_9, "DBpedia 3.9"))]
    return default_index, other_indices


def get_all_methods(service_label):
    """Given a service_label label, returns all the available methods to choose among, and the default one.

    :param service_label: a service_label label constant in [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, \
    SERVICE_TTI].
    :return:
    """
    if service_label is SERVICE_E_RETRIEVAL:
        default_method = (ER_METHOD_FALLBACK, METHOD_2_HUMAN_LABEL.get(ER_METHOD_FALLBACK, "Elastic"))
        other_methods = []
    elif service_label is SERVICE_E_LINKING:
        default_method = (EL_METHOD_FALLBACK, METHOD_2_HUMAN_LABEL.get(EL_METHOD_FALLBACK, "Commonness"))
        other_methods = []
    elif service_label is SERVICE_TTI:
        default_method = (TTI_METHOD_FALLBACK_TC, METHOD_2_HUMAN_LABEL.get(TTI_METHOD_FALLBACK_TC, "Type-centric"))
        other_methods = [("entity_centric", "Entity-centric")]
    return default_method, other_methods


def init_service(service_label, index_name=None, method=None):
    """Returns an ServiceWrapper object, initialized with default configuration data from server-side, unless optional \
    configuration items are provided.

    :param service_label: a service_label label constant in [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, \
    SERVICE_TTI].
    :param index_name:
    :param method:
    :return:
    """
    selected_index, other_indices = get_all_indices(service_label)  # initialization with default settings
    if index_name and index_name != selected_index[0]:  # replace that default selected index with the required one
        new_index = (index_name, INDEX_2_HUMAN_LABEL.get(index_name, index_name))
        other_indices = list(filter(lambda e: e != new_index, other_indices))  # remove the new selected one from others
        other_indices += [selected_index]  # and add back the old selected one as one of the possible others
        selected_index = new_index  # set up the new selected one

    # Proceed analogously for methods
    selected_method, other_methods = get_all_methods(service_label)
    if method and method != selected_method[0]:
        new_method = (method, METHOD_2_HUMAN_LABEL.get(method, method))
        other_methods = list(filter(lambda e: e != new_method, other_methods))
        other_methods += [selected_method]
        selected_method = new_method

    return ServiceWrapper(service_label, selected_index, other_indices, selected_method, other_methods,
                          default_html_names=True)


def init_services():
    """Returns a list of initial service configurations (ServiceWrapper instances)."""
    services = []  # It will be a list of initial service configurations

    for service_label in SERVICES_TO_PROVIDE:
        services.append(init_service(service_label))

    return services


# -----------------
# Results processing

def __strip_angle_brackets(prefixed_str):
    """Strips prefixed_str from sorrounding angle brackets."""
    return prefixed_str[1:-1] if len(prefixed_str) > 1 and prefixed_str.startswith("<") else prefixed_str


def __get_prefix(stripped_prefixed_str):
    return stripped_prefixed_str.split(":")[0] if ":" in stripped_prefixed_str else stripped_prefixed_str


def __get_payload(stripped_prefixed_str):
    return stripped_prefixed_str.split(":")[1] if ":" in stripped_prefixed_str else stripped_prefixed_str


def __convert_from_camelcase(phrase):
    """Splits a CamelCased string into a new one, with each word capitalized, where words are separated by blanks.

    :param phrase: a possibly CamelCased string.
    :return:
    """
    # http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s1 = re_sub('(.)([A-Z][a-z]+)', r'\1_\2', phrase)
    with_blanks = str(re_sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace("_", " ").capitalize())
    return " ".join([w.capitalize() for w in with_blanks.split(" ")])


def __shorten_abstract(abstract, max_length=MAX_ABSTRACT_LEN):
    """Returns a possibly shorter version of the abstract, such that it takes at the most around 500 chars."""
    ret = abstract
    if len(ret) > max_length:
        sentences = ret.split(".")
        fst_sentence = sentences[0]  # Always 1 sentence at least :P
        if len(fst_sentence) > max_length:  # but some abstracts are bad, too long,...
            chunk = abstract[:max_length]  # ... so just pick some initial chunk...
            ret = " ".join(chunk.split(" ")[:-1]) + "..."  # ...with nice ending dots after the last complete word.
        else:
            short = fst_sentence
            for i in range(1, len(sentences)):  # let's add sentences keeping total len below max
                if len(short + sentences[i]) > max_length:
                    break
                short += sentences[i]
            ret = short
    if len(ret) > 0 and not ret.endswith("."):
        ret += "."
    return ret


def __sort_set_of_str_elems(elems):
    """Returns a sorted list of the strings contained in elems.

    :param elems: set of strings
    :return:
    """
    return [str(x) for x in sorted(map(lambda x: int(x), list(elems)))]


# -------
# Card results

def __get_card_item(catalog_results, possible_properties, prefix=False):
    """Searches for finding the first matching property among a list of possible ones, ad return """
    item = None
    for prop in possible_properties:
        if prefix:
            prop = "<dbo:{}>".format(prop)
            # pick the first found property
            l = catalog_results.get(prop, [])
            if len(l) > 0:  # found
                item = l[0]
                break
            prop = "<dbp:{}>".format(prop)
            # pick the first found property
            l = catalog_results.get(prop, [])
            if len(l) > 0:  # found
                item = l[0]
                break
        else:
            # pick the first found property
            l = catalog_results.get(prop, [])
            if len(l) > 0:  # found
                item = l[0]
                break

    return item


def __get_card_picture(catalog_results):
    """Gets the entity picture if available."""
    POSSIBLE_PICTURE_PROPS = ["<dbo:thumbnail>", "<foaf:depiction>"]  # sorted decreasingly by importance
    picture = __get_card_item(catalog_results, POSSIBLE_PICTURE_PROPS)
    return __strip_angle_brackets(picture) if picture else picture


def __get_card_type(catalog_results):
    """Gets the most specific type of the entity."""
    POSSIBLE_TYPE_PROPS = ["<dbo:type>", "<rdf:type>", "<dbo:status>"]  # sorted decreasingly by importance
    TYPE_PROP_PREFIXES = ["schema", "dbo", "dbpedia", "rdf", "foaf", "geo", "owl"]  # idem by importance; excluding "wd"

    type = None
    for prop in POSSIBLE_TYPE_PROPS:
        if type is not None:
            break
        # pick the first found property
        l = catalog_results.get(prop, [])
        if len(l) > 0:  # found, now pick first one useful
            for type_prop_prefix in TYPE_PROP_PREFIXES:
                if type is not None:  # already found with a prefix, so stop
                    break
                for possible_type in l:
                    possible_type = __strip_angle_brackets(possible_type)
                    prefix = __get_prefix(possible_type)
                    payload = __get_payload(possible_type)
                    if payload.startswith("Wikidata"):
                        continue
                    if prefix == type_prop_prefix:
                        type = __convert_from_camelcase(payload)
                        break  # important
            break

    return type


def __get_card_description(catalog_results):
    """Gets a short description (or alias, or motto), o.w. an official name for the entity if available.."""
    POSSIBLE_DESCRIPTION_PROPS = ["<dbp:shortDescription>",
                                  "<dbp:nickname>",  # no particular importance, but nickname seems more standard
                                  "<dbp:motto>",
                                  "<dbo:alias>",
                                  "<dbp:officialName>",  # officialName may likely be same as name, that's why is low
                                  # "<foaf:name>"
                                  ]  # sorted decreasingly by importance
    return __get_card_item(catalog_results, POSSIBLE_DESCRIPTION_PROPS)


def __get_card_homepage(catalog_results):
    """Gets the entity homepage if available."""
    POSSIBLE_HOMEPAGE_PROPS = ["<foaf:homepage>",
                               "<dbp:website>",
                               # "<dbp:url>"  # likely noisy catalog attr
                               ]  # sorted decreasingly by importance
    homepage = __get_card_item(catalog_results, POSSIBLE_HOMEPAGE_PROPS)
    return __strip_angle_brackets(homepage) if homepage else homepage


def __final_value_prettifying(value, possible_prop):
    """Prettifies a very precise float string by rounding it."""
    if possible_prop == "Work/runtime":
        value = str(round(float(value), 2))


def __find_props(catalog_results, props_to_find, candidate_props, found_props_pairs, already_used_props, prefix=False,
                 not_final_break=False, icon=None, icon_map=None):
    for possible_prop in candidate_props:
        if len(props_to_find) == 0:  # nothing to do
            break
        if possible_prop in already_used_props:  # avoid repeating a prop
            continue
        value = __get_card_item(catalog_results, [possible_prop], prefix=prefix)
        if value:
            # Some noise filtering
            if value == "":
                continue
            if value.startswith("<"):
                value = __get_payload(__strip_angle_brackets(value))

            # Prettify attr and value; find icon if needed
            clean_attr = __convert_from_camelcase(__get_payload(__strip_angle_brackets(possible_prop)))
            if possible_prop == "<georss:point>":
                clean_attr = "Geo coordinates"
            value = value.replace("_", " ")
            # value = __final_value_prettifying(value, possible_prop)  # too much overhead for a very unlikely fixing
            if icon_map:
                icon = icon_map.get(possible_prop, None)  # NOTE: default is None so template doesn't show it

            # Add found attr-value pair; remove since one less to find; keep track of prop to avoid repetitions
            found_props_pairs[props_to_find[0]] = (clean_attr, value, icon)
            props_to_find.pop(0)  # pop from list head side
            already_used_props.append(possible_prop)
            if not not_final_break:  # else: NOT break here: run for until all needed props are found
                break  # only 1 prop and done


def __get_card_properties(catalog_results):
    """Tries to find at the most 3 properties of the entity: 1 date-related if possible, 1 location-related if \
    possible, and filling the missing ones with other interesting properties."""
    found_props_pairs = dict()

    props_to_find = ["prop_1", "prop_2", "prop_3"]  # to be popped when finding
    already_used_props = []  # to avoid repetitions

    # Look for date-related properties...
    __find_props(catalog_results, props_to_find, POSSIBLE_DATE_PROPS, found_props_pairs, already_used_props,
                 prefix=True, icon=FAVICON_CAL)

    # ...then for place- and location-related properties...
    __find_props(catalog_results, props_to_find, ["<georss:point>"], found_props_pairs, already_used_props,
                 icon=FAVICON_MAP_MARKER)
    __find_props(catalog_results, props_to_find, POSSIBLE_PLACE_PROPS + POSSIBLE_LOCATION_PROPS, found_props_pairs,
                 already_used_props, prefix=True, icon=FAVICON_MAP_MARKER)

    # ...then for other interesting properties...
    __find_props(catalog_results, props_to_find, POSSIBLE_OTHER_INTERESTING_PROPS, found_props_pairs,
                 already_used_props, prefix=True, not_final_break=True, icon_map=PROPS_ICONS)

    return found_props_pairs


def __obtain_card_data(catalog_results):
    """Returns a dict with data for making an entity card."""
    card_data = dict()

    picture = __get_card_picture(catalog_results)
    if picture:
        card_data["picture"] = picture

    type = __get_card_type(catalog_results)
    if type:
        card_data["type"] = type

    description = __get_card_description(catalog_results)
    if description:
        card_data["description"] = description

    homepage = __get_card_homepage(catalog_results)
    if homepage:
        card_data["homepage"] = homepage

    card_data["properties"] = __get_card_properties(catalog_results)

    return card_data


def __must_be_skipped(type_id):
    """Assesses whether a typeID must be skipped."""
    return type_id.startswith("<dbo:Wikidata:")


def process_results(raw_results, service_label, protocol="http:/", server_hostname_api="", entity_collection="",
                    request_timeout=30):
    """Processes a list of raw results to obtain further data components.

    :param raw_results: a list of raw results (typically docIDs).
    :param service_label: a constant for the required service_label.
    :return:
    """
    results = []

    if service_label is SERVICE_E_RETRIEVAL:
        sorted_ranks = __sort_set_of_str_elems(raw_results.get("results", {}).keys())
        for rank in sorted_ranks:
            result_dict = raw_results.get("results", {}).get(rank, {})
            entity_id = result_dict.get("entity", "")
            if entity_id == "":
                continue

            unprefixed_doc_id = entity_id.split(":")[-1].split(">")[0]

            abstract_list = result_dict.get("fields", {}).get("abstract", [])
            abstract = abstract_list[0] if len(abstract_list) > 0 else ""

            # Entity catalog request for making entity cards and getting Freebase ID
            url = "/".join([protocol, server_hostname_api, "ec", entity_id])
            try:
                # print("\tCatalog request' URL: {}".format(url))
                r = requests_get(url, timeout=request_timeout)
                catalog_results = j_loads(r.text)
            except:
                catalog_results = dict()

            card_data = __obtain_card_data(catalog_results)

            # Final result dict
            result = {RESULT_DOC_TITLE_K: unprefixed_doc_id.replace("_", " "),
                      RESULT_DOC_ID_K: entity_id,
                      RESULT_DOC_SNIPPET_K: __shorten_abstract(abstract),
                      RESULT_URL_DBPEDIA_K: "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label],
                                                      unprefixed_doc_id]),
                      RESULT_URL_WIKIPEDIA_K: "/".join([WIKIPEDIA_HOSTNAME, SERVICE_TO_WIKIPEDIA_SUBHOST[service_label],
                                                        unprefixed_doc_id]),

                      RESULT_FREEBASE_ID_K: catalog_results.get("fb:<owl:sameAs>", [None])[0],
                      RESULT_DOC_CARD_K: card_data
                      }

            results.append(result)

    elif service_label is SERVICE_E_LINKING:
        query = raw_results.get("processed_query", {})
        linked_results = raw_results.get("results", {})

        result_counter = 0
        for linked_substr, result_l in sorted(linked_results.items(), reverse=True, key=lambda item: item[1][1]):
            result_counter += 1
            entity_id = result_l[0]
            score = result_l[1]
            unprefixed_doc_id = entity_id.split(":")[-1].split(">")[0]
            entity_url = "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label], unprefixed_doc_id])

            # Entity catalog request for getting popup picture and abstract
            url = "/".join([protocol, server_hostname_api, "ec", entity_id])
            try:
                # print("\tCatalog request' URL: {}".format(url))
                r = requests_get(url, timeout=request_timeout)
                catalog_results = j_loads(r.text)
            except:
                catalog_results = dict()

            # Defining result components
            picture = __get_card_picture(catalog_results)  # possibly None
            most_specific_type = __get_card_type(catalog_results)  # possibly None
            if most_specific_type:
                most_specific_type = most_specific_type.upper()
            abstract = __shorten_abstract(catalog_results.get("<dbo:abstract>", [""])[0], max_length=400)
            formatted_result = query.replace(
                linked_substr,
                "<a href=\"{}\" target=\"_blank\" id=\"elLink{}\" "
                "onmouseover=\"showPop(\'elPop{}\', event);\""
                " onmouseout=\"hidePop(\'elPop{}\');\""  # NOTE: important the blank between each event handler
                ">"
                "{}</a>".format(entity_url, result_counter, result_counter, result_counter, linked_substr))

            result = {RESULT_LINKED_SUBSTR_K: linked_substr,
                      RESULT_DOC_TITLE_K: unprefixed_doc_id.replace("_", " "),
                      RESULT_DOC_ID_K: entity_id[1:-1] if len(entity_id) > 1 else "",
                      RESULT_DOC_SNIPPET_K: abstract,
                      RESULT_DOC_PICTURE_K: picture,
                      RESULT_URL_DBPEDIA_K: entity_url,
                      RESULT_DOC_SCORE_K: round(score, 6),
                      RESULT_DOC_TYPE_K: most_specific_type,
                      RESULT_EL_TO_SHOW_K: formatted_result
                      }

            results.append(result)

    elif service_label is SERVICE_TTI:

        # TODO remap to exp the TTI scores from API when method is LM

        sorted_ranks = __sort_set_of_str_elems(raw_results.get("results", {}).keys())
        for rank in sorted_ranks[0:10]:
            result_dict = raw_results.get("results", {}).get(rank, {})
            type_id = result_dict.get("type", "")

            if __must_be_skipped(type_id):
                continue
            unprefixed_doc_id = type_id.split(":")[-1].split(">")[0]
            result = {RESULT_DOC_TITLE_K: __convert_from_camelcase(unprefixed_doc_id).replace("_", " "),
                      RESULT_DOC_ID_K: type_id,
                      RESULT_DOC_SCORE_K: round(result_dict.get("score", 0), 6),
                      RESULT_URL_DBPEDIA_K: "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label],
                                                      unprefixed_doc_id])
                      }

            results.append(result)

    return results
