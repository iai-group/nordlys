"""Web Interface service utilities.

service_utils
--------------

@author: Dario Garigliotti
"""

from re import sub as re_sub

# -----------------
# -----------------
#  Constants
# -----------------

# -------
# Services
# TODO define all
# NOTE: not only used as constants to distinguish among services here in service_utils module, but their actual strings
# are the same as used in service URLs so we use them for generalizing some templates, e.g. the pagination one.
SERVICE_E_RETRIEVAL = "er"
SERVICE_E_LINKING = "el"
SERVICE_TTI = "tti"

SERVICES_TO_PROVIDE = [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, SERVICE_TTI]  # TODO add

# -------
# Indices
# TODO add if needed
ER_INDEX_FALLBACK_2015_10 = "nordlys_dbpedia_2015_10"
ER_INDEX_TOY = "toy_index"
EL_INDEX_FALLBACK = ""  # TODO ?
TTI_INDEX_FALLBACK_2015_10 = "dbpedia_2015_10_types_bm25"
TTI_INDEX_DBPEDIA_3_9 = "dbpedia_3_9_types_bm25"
# -------
# Methods
# TODO add if needed
ER_METHOD_FALLBACK = "elastic"  # TODO fix
EL_METHOD_FALLBACK = ""  # TODO ?
TTI_METHOD_FALLBACK_TC = "type_centric"
TTI_METHOD_EC = "entity_centric"

# -------
# DBpedia settings
DBPEDIA_HOSTNAME = "http://dbpedia.org"
SERVICE_TO_DBPEDIA_SUBHOST = {SERVICE_E_RETRIEVAL: "page",
                              SERVICE_E_LINKING: "page",
                              SERVICE_TTI: "ontology"}

# -------
# Search results fields
# TODO add if needed
RESULT_DOC_TITLE_K = "doc_title"
RESULT_DOC_ID_K = "doc_id"
RESULT_URL_K = "doc_url"
RESULT_DOC_SNIPPET_K = "doc_snippet"
RESULT_DOC_SCORE_K = "doc_score"
RESULT_LINKED_SUBSTR_K = "linked_substring"
RESULT_EL_TO_SHOW_K = "el_formatted_result_to_show"
# -------
# Human-readable labels
INDEX_2_HUMAN_LABEL = {ER_INDEX_FALLBACK_2015_10: "DBpedia 2015-10",  # ER...
                       ER_INDEX_TOY: "Toy Index :)",
                       TTI_INDEX_FALLBACK_2015_10: "DBpedia 2015-10",  # TTI...
                       TTI_INDEX_DBPEDIA_3_9: "DBpedia 3.9"
                       }

METHOD_2_HUMAN_LABEL = {ER_METHOD_FALLBACK: "Elastic",  # TODO fix
                        EL_METHOD_FALLBACK: "",  # TODO ?
                        TTI_METHOD_FALLBACK_TC: "Type-centric"
                        }

# -------
# Additional
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


def get_all_indices(service_label):
    """Given a service_label label, returns all the available indices to choose among, and the default one.

    :param service_label: a service_label label constant in [SERVICE_E_RETRIEVAL, SERVICE_E_LINKING, \
    SERVICE_TTI].
    :return:
    """

    # TODO it could call somehow the API to know the indices, for now it's hardcoded
    if service_label is SERVICE_E_RETRIEVAL:
        default_index = (
            ER_INDEX_FALLBACK_2015_10, INDEX_2_HUMAN_LABEL.get(ER_INDEX_FALLBACK_2015_10, "DBpedia 2015-10"))
        other_indices = [(ER_INDEX_TOY, INDEX_2_HUMAN_LABEL.get(ER_INDEX_TOY, "Toy Index :)"))]
    elif service_label is SERVICE_E_LINKING:
        default_index = (EL_INDEX_FALLBACK, "Index")  # TODO fix
        other_indices = [("another_index", "Another Index")]  # TODO fix
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
    # TODO extend param list after adding services

    # TODO it could call somehow the API to know the indices, for now it's hardcoded
    if service_label is SERVICE_E_RETRIEVAL:
        default_method = (ER_METHOD_FALLBACK, METHOD_2_HUMAN_LABEL.get(ER_METHOD_FALLBACK, "Elastic"))
        other_methods = [("other_er_1", "Other search method 1"), ("other_er_2", "Other search method 2")]  # TODO
    elif service_label is SERVICE_E_LINKING:
        default_method = (EL_METHOD_FALLBACK, METHOD_2_HUMAN_LABEL.get(EL_METHOD_FALLBACK, "Method"))  # TODO fix
        other_methods = [("other_el_1", "Other entity linking method 1"),
                         ("other_el_2", "Other entity linking method 2")]
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


def __convert_from_camelcase(phrase):
    """Splits a CamelCased string into a new one, with each word capitalized, where words are separated by blanks.

    :param phrase: a possibly CamelCased string.
    :return:
    """
    # http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s1 = re_sub('(.)([A-Z][a-z]+)', r'\1_\2', phrase)
    with_blanks = str(re_sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower().replace("_", " ").capitalize())
    return " ".join([w.capitalize() for w in with_blanks.split(" ")])


def __shorten_abstract(abstract):
    """Returns a possibly shorter version of the abstract, such that it takes at the most around 500 chars."""
    ret = abstract
    if len(ret) > MAX_ABSTRACT_LEN:
        sentences = ret.split(".")
        fst_sentence = sentences[0]  # Always 1 sentence at least :P
        if len(fst_sentence) > MAX_ABSTRACT_LEN:  # but some abstracts are bad, too long,...
            chunk = abstract[:MAX_ABSTRACT_LEN]  # ... so just pick some initial chunk...
            ret = " ".join(chunk.split(" ")[:-1]) + "..."  # ...with nice ending dots after the last complete word.
        else:
            short = fst_sentence
            for i in range(1, len(sentences)):  # let's add sentences keeping total len below max
                if len(short + sentences[i]) > MAX_ABSTRACT_LEN:
                    break
                short += sentences[i]
            ret = short
    return ret


# def process_results(raw_results, service_label):
#     """Processes a list of raw results to obtain further data components.
#
#     :param raw_results: a list of raw results (typically docIDs).
#     :param service_label: a constant for the required service_label.
#     :return:
#     """
#     results = []
#
#     if service_label is SERVICE_E_RETRIEVAL:
#         for r in raw_results:
#             unprefixed_doc_id = r.get("_id", "").split(":")[-1].split(">")[0]
#             result = {RESULT_DOC_TITLE_K: unprefixed_doc_id.replace("_", " "),
#                       RESULT_DOC_ID_K: r.get("_id", ""),
#                       RESULT_URL_K: "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label],
#                                               unprefixed_doc_id]),
#                       RESULT_DOC_SNIPPET_K: __shorten_abstract(r.get("_source", {}).get("abstract", ""))
#                       }
#
#             results.append(result)
#
#     elif service_label is SERVICE_TTI:
#         raw_results = raw_results[0:10]  # ensure only top 10 results
#         for r in raw_results:
#             unprefixed_doc_id = r.get("_id", "").split(":")[-1].split(">")[0]
#             result = {RESULT_DOC_TITLE_K: __convert_from_camelcase(unprefixed_doc_id),
#                       RESULT_DOC_ID_K: r.get("_id", ""),
#                       RESULT_DOC_SCORE_K: r.get("_score", 0)
#                       }
#
#             results.append(result)
#
#     return results


def __sort_set_of_str_elems(elems):
    """Returns a sorted list of the strings contained in elems.

    :param elems: set of strings
    :return:
    """
    return [str(x) for x in sorted(map(lambda x: int(x), list(elems)))]


def process_results(raw_results, service_label):
    """Processes a list of raw results to obtain further data components.

    :param raw_results: a list of raw results (typically docIDs).
    :param service_label: a constant for the required service_label.
    :return:
    """
    results = []

    if service_label is SERVICE_E_RETRIEVAL:
        sorted_ranks = __sort_set_of_str_elems(raw_results.get("results", {}).keys())
        print(sorted_ranks)
        for rank in sorted_ranks:
            result_dict = raw_results.get("results", {}).get(rank, {})
            entity_id = result_dict.get("entity", "")
            if entity_id == "":
                continue

            unprefixed_doc_id = entity_id.split(":")[-1].split(">")[0]
            abstract_list = result_dict.get("fields", {}).get("abstract", [])
            abstract = abstract_list[0] if len(abstract_list) > 0 else ""
            result = {RESULT_DOC_TITLE_K: unprefixed_doc_id.replace("_", " "),
                      RESULT_DOC_ID_K: entity_id,
                      RESULT_DOC_SNIPPET_K: __shorten_abstract(abstract),
                      RESULT_URL_K: "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label],
                                              unprefixed_doc_id])
                      }

            results.append(result)

    elif service_label is SERVICE_E_LINKING:
        query = raw_results.get("processed_query", {})
        linked_results = raw_results.get("results", {})
        print("linked_results = {}".format(linked_results))

        result_counter = 0
        for linked_substr, result_l in sorted(linked_results.items(), reverse=True, key=lambda item: item[1][1]):
            result_counter += 1
            entity_id = result_l[0]
            score = result_l[1]
            unprefixed_doc_id = entity_id.split(":")[-1].split(">")[0]
            entity_url = "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label], unprefixed_doc_id])

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
                      RESULT_URL_K: entity_url,
                      RESULT_DOC_SCORE_K: round(score, 6),
                      RESULT_EL_TO_SHOW_K: formatted_result
                      }
            pass

            results.append(result)

        print("results = {}".format(results))

    # elif service_label is SERVICE_TTI: # TODO NOTE: use this when TTI is from Elastic
    #     raw_results = raw_results.get("hits", {}).get("hits", [])
    #     raw_results = raw_results[0:10]  # ensure only top 10 results
    #     for r in raw_results:
    #         unprefixed_doc_id = r.get("_id", "").split(":")[-1].split(">")[0]
    #         result = {RESULT_DOC_TITLE_K: __convert_from_camelcase(unprefixed_doc_id),
    #                   RESULT_DOC_ID_K: r.get("_id", ""),
    #                   RESULT_DOC_SCORE_K: r.get("_score", 0)
    #                   }
    #
    #         results.append(result)

    elif service_label is SERVICE_TTI:  # TODO NOTE: use this when TTI is from API

        # TODO remap to exp the TTI scores from API when method is LM

        sorted_ranks = __sort_set_of_str_elems(raw_results.get("results", {}).keys())
        for rank in sorted_ranks[0:10]:
            result_dict = raw_results.get("results", {}).get(rank, {})
            type_id = result_dict.get("type", "")

            unprefixed_doc_id = type_id.split(":")[-1].split(">")[0]
            result = {RESULT_DOC_TITLE_K: unprefixed_doc_id.replace("_", " "),
                      RESULT_DOC_ID_K: type_id,
                      RESULT_DOC_SCORE_K: round(result_dict.get("score", 0), 6),
                      RESULT_URL_K: "/".join([DBPEDIA_HOSTNAME, SERVICE_TO_DBPEDIA_SUBHOST[service_label],
                                              unprefixed_doc_id])
                      }

            results.append(result)

    return results
