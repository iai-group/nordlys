"""
instances
---------

Instances used for Machine learning algorithms.

    - Manages a set of Instance objects
    - Loads instance-data from JSON or TSV files
        - When using TSV, instance properties, target, and features are loaded from separate files
    - Generates a list of instances in JSON or RankLib format

@author: Faegheh Hasibi
@author: Krisztian Balog
"""

import csv
import json
from sys import argv

from collections import defaultdict
from nordlys.core.ml.instance import Instance


class Instances(object):
    """
    Class attributes:
        instances: Instance objects stored in a dictionary indexed by instance id
    """

    def __init__(self, instances=None):
        """
        :param instances: instances in a list or dict
            - if list then list index is used as the instance ID
            - if dict then the key is used as the instance ID
        """
        self.__instances = {}

        if type(instances) == list:
            for ins in instances:
                self.add_instance(ins)

        elif type(instances) == dict:
            self.__instances = instances

    def append_instances(self, ins_list):
        """Appends the list of Instances objects.

        :param ins_list: list of Instance objects
        """
        for ins in ins_list:
            self.add_instance(ins)

    def add_instance(self, instance):
        """Adds an Instance object to the list of instances.

        :param instance: Instance object
        """
        self.__instances[instance.id] = instance

    def get_instance(self, instance_id):
        """Returns an instance by instance id.

        :param instance_id: (string)
        :return: Instance object
        """
        return self.__instances.get(instance_id, None)

    def get_all(self):
        """Returns list of all instances."""
        return list(self.__instances.values())

    def get_all_ids(self):
        """Returns list of all instance ids."""
        return list(self.__instances.keys())

    def __load_from_tsv(self, tsv_file, type, params):
        """Loads instances from a TSV file.

        :param tsv_file: name of the TSV file
        :param type: type of the data: "properties", "features" or "target"
        :param params: list of columns mapped to properties or features
        """
        with open(tsv_file, "rb") as tsvfile:
            reader = csv.DictReader(tsvfile, delimiter="\t", quoting=csv.QUOTE_NONE)
            # print "Processing gold file with following fields:\n" + str(reader.fieldnames)

            # Checks all the params are in the TSV file header
            if set(params) != set(reader.fieldnames[1:]):
                raise Exception("TSV header does not match params \"" + ",".join(params) + "\" in file:\n\t" + tsv_file)

            # Reads tsv lines
            for line in reader:
                ins_id = line["id"]

                # Generating instance
                if ins_id in self.__instances:  # existing instance
                    ins = self.get_instance(ins_id)
                else:  # new instance
                    ins = Instance(ins_id)
                    self.add_instance(ins)

                # adding params
                for param in params:
                    if type == "properties":
                        ins.add_property(param, line[param])
                    elif type == "features":
                        ins.add_feature(param, line[param])
                    elif type == "target":
                        ins.target = line[param]

    def add_properties_from_tsv(self, tsv_file, properties):
        self.__load_from_tsv(tsv_file, "properties", properties)

    def add_features_from_tsv(self, tsv_file, features):
        self.__load_from_tsv(tsv_file, "features", features)

    def add_target_from_tsv(self, tsv_file):
        self.__load_from_tsv(tsv_file, "target", ["target"])

    @classmethod
    def from_json(cls, json_file):
        """Loads instances from a JSON file.

        :param json_file: (string)
        :return Instances object
        """
        print("Reading JSON file " + json_file + " ...")
        json_data = open(json_file)
        data = json.load(json_data)
        instance_list = []
        # read instances
        for ins_id, fields in data.items():
            instance = Instance.from_json(ins_id, fields)
            instance_list.append(instance)
        return cls(instance_list)

    def group_by_property(self, property):
        """Groups instances by a given property.

        :param property
        :return a dictionary of instance ids {id:[ml.Instance, ...], ...}
        """
        property_dict = defaultdict(list)
        for ins in self.get_all():
            property_dict[ins.get_property(property)].append(ins)
        return property_dict

    # todo: find efficient way of writing json file
    def to_json(self, json_file=None):
        """ Converts all instances to JSON and writes it to the file

        :param json_file: (string)
        :return: JSON dump of all instances.
        """
        inss_json = {}
        for ins in self.get_all():
            inss_json.update(ins.to_json())
        if json_file is not None:
            # print "Writing JSON format of instances ..."
            out = open(json_file, "w")
            json.dump(inss_json, out, indent=4)
            print("JSON output:\t" + json_file)
        return inss_json

    def to_str(self, file_name=None):
        """ Converts instances to string and write them to the given file.
        :param file_name
        :return: String format of instances
        """
        out_file = None
        if file_name is not None:
            open(file_name, "w").close()  # cleans previous contents
            out_file = open(file_name, "a")

        counter = 0
        out = ""
        for ins in self.get_all():
            out += ins.to_str() + "\n"
            counter += 1
            # append instances to the file
            if (counter % 1000) == 0:
                # print "Converting is done until instance " + str(ins.id)
                if out_file is not None:
                    out_file.write(out)
                    out = ""
        if out_file is not None:
            out_file.write(out)
            print("String output:\t" + file_name)
            return None
        return out

    def to_libsvm(self, file_name=None, qid_prop=None):
        """
        Converts all instances to the LibSVM format and writes them to the file.
        - Libsvm format:
            <line> .=. <target> qid:<qid> <feature>:<value> ... # <info>
            <target> .=. <float>
            <qid> .=. <positive integer>
            <feature> .=. <positive integer>
            <value> .=. <float>
            <info> .=. <string>
        - Example: 3 qid:1 1:1 2:1 3:0 4:0.2 5:0 # 1A

        NOTES:
            - The property used for qid(qid_prop) should hold integers
            - For pointwise algorithms, we use instance id for qid
            - Lines in the RankLib input have to be sorted by increasing qid.

        :param file_name: File to write libsvm format of instances.
        :param qid_prop: property to be used as qid. If none,
        """
        # If no entity matches query
        if len(self.__instances) == 0:
            print("No instance is created!!")
            open(file_name, "w").write("")
            return ""

        # Getting features
        ins = next(iter(self.__instances.values()))
        features = sorted(list(ins.features.keys()))

        # cleans previous contents
        open(file_name, "w").close()
        out_file = open(file_name, "a")

        # Adding feature names as header of libsvm file
        out = "# target instance_Id"
        for feature in features:
            out += " " + feature
        out += "\n"

        # sort instances by qid
        if qid_prop is None:
            sorted_instances = sorted(self.get_all(), key=lambda ins: int(ins.id))
        else:
            sorted_instances = sorted(self.get_all(), key=lambda ins: int(ins.get_property(qid_prop)))

        counter = 0
        print("Converting instances to ranklib format ...")
        for ins in sorted_instances:
            out += ins.to_libsvm(features, qid_prop) + "\n"
            counter += 1
            # write the instances to the file
            if (counter % 1000) == 0:
                out_file.write(out)
                out = ""
                # print "Converting is done until instance " + str(ins.id)
        out_file.write(out)
        print("Libsvm output:\t" + file_name)

    def add_qids(self, prop):
        """
        Generates (integer) q_id-s (for libsvm) based on a given (non-integer) property.
        It assigns a unique integer value to each different value for that property.

        :param prop: name of the property.
        :return:
        """
        prop_ids = {}
        for ins in self.get_all():
            p = ins.get_property(prop)
            if p in prop_ids:
                q_id = prop_ids[p]
            else:
                q_id = len(prop_ids) + 1
                prop_ids[p] = q_id
            ins.add_property("q_id", q_id)


def main(args):
    inss = Instances()
    # we assume that the 1st column is always the ins_id (unique)
    # the list specifies which property or feature the column value should be loaded to; columns with None are ignored
    # one file with properties
    inss.add_properties_from_tsv(args[0], ["sequence"])
    # one or more files with features
    inss.add_features_from_tsv(args[1], ["sentence_length", "article_length", "sentence_order", "predicate_tense"])
    # inss.add_features_from_tsv(feat_file_2, ["feature4"])
    # inss.add_features_from_tsv(feat_file_3, ["feature5", "feature6"])
    # one with target value
    inss.add_target_from_tsv(args[2])
    print(inss.to_str())
    inss.to_json("data/maff.json")


    # *** These lines are used for converting a json file to libsvm format. ***
    # # load from json file
    # inss = Instances.from_json("data/ml/maff.json")
    # # add q_id -s based on transaction_id
    # inss.add_qids("transaction_id")
    # # write q_id property back to json file
    # inss.to_json("data/ml/maff2.json")
    # # write to libsvm file
    # inss.to_libsvm("data/ml/maff.libsvm", "q_id")


if __name__ == "__main__":
    main(argv[1:])
