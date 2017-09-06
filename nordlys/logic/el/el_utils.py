"""
EL Utils
========

Utility methods for entity linking.

Author: Faegheh Hasibi
"""
from nordlys import config
from nordlys.config import PLOGGER


def load_kb_snapshot(kb_file):
    """Loads DBpedia Snapshot of proper name entities (used for entity linking)."""
    if config.KB_SNAPSHOT is None:
        PLOGGER.info("Loading KB snapshot of proper named entities ...")
        kb_snapshot = set()
        with open(kb_file, "r") as f:
            for line in f:
                kb_snapshot.add(line.strip())
        config.KB_SNAPSHOT = kb_snapshot


def is_name_entity(en_id):
    """Returns true if the entity is considered as proper name entity."""
    if (config.KB_SNAPSHOT is not None) and (en_id not in config.KB_SNAPSHOT):
        return False
    return True


def to_elq_eval(annotations, output_file):
    """Write entity annotations to ELQ evaluation format.

    :param linked_ens: {qid:[{"mention":xx, "entity": yy, "score":zz}, ..], ..}
    """
    out_str = ""
    for qid, q_annots in sorted(annotations.items()):
        for annot in q_annots:
            out_str += qid + "\t1\t" + annot["entity"] + "\n"
    open(output_file, "w").write(out_str)
    PLOGGER.info("ELQ evaluation file: " + output_file)
