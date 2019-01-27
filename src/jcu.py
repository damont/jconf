#!/user/bin/python
"""Credit to David Monts, circa 2017

The JSON Class Utility!!!

For more information, python jcu.py -h
"""

import argparse
import json
from classMaker import ClassMaker
from makerFactory import MakerFactory

class Jcu(object):
    """The Jcu class can be ran either as a stand-alone CLI for creating the different
    classes or used in conjuction with the JSON Class Designer.
    """

    def __init__(self):
        """Initialize our list of class tuples!!!
        """
        self.classes = []

    def create_classes_dirty(self, json_dictionary, json_class_name, lang):
        """Parse through the passed in dictionary and create the class from it.

        Args:
            json_dictionary - The JSON formatted dictionary.
            json_class_name - The name that will be the class name
            lang - The desired programming language for the output
        """
        del self.classes[:]
        self._parse_raw_json(json_dictionary, json_class_name, lang)
        return self.classes

    def _parse_raw_json(self, json_dictionary, json_class_name, lang):
        """Add the different attributes to a classMaker object.

        Args:
            json_dictionary - The JSON formatted dictionary
            json_class_name - The name for the class
            lang - The desired programming language for the output
        """
        class_maker = MakerFactory.get_maker(lang, json_class_name)
        if class_maker:
            for key in json_dictionary:
                if isinstance(json_dictionary[key], dict):
                    class_maker.add_class(key)
                    self._parse_raw_json(json_dictionary[key], key, lang)
                if isinstance(json_dictionary[key], str):
                    class_maker.add_string(key, json_dictionary[key])
                if isinstance(json_dictionary[key], float):
                    class_maker.add_number(key, json_dictionary[key])
                if isinstance(json_dictionary[key], int):
                    class_maker.add_number(key, float(json_dictionary[key]))
                if isinstance(json_dictionary[key], list):
                    if json_dictionary[key]:
                        if isinstance(json_dictionary[key], dict):
                            class_maker.add_list(key, ClassMaker.Types.CLASS)
                            self._parse_raw_json(json_dictionary[key][0], key, lang)
                        if isinstance(json_dictionary[key], str):
                            class_maker.add_list(key, ClassMaker.Types.STRING)
                        if isinstance(json_dictionary[key], int) or \
                           isinstance(json_dictionary[key], float):
                            class_maker.add_list(key, ClassMaker.Types.DOUBLE)
                        if isinstance(json_dictionary[key], list):
                            class_maker.add_list(key, ClassMaker.Types.ARRAY)
                        if isinstance(json_dictionary[key], bool):
                            class_maker.add_list(key, ClassMaker.Types.BOOLEAN)
                if isinstance(json_dictionary[key], bool):
                    class_maker.add_boolean(key, json_dictionary[key])
            self.classes.extend(class_maker.stringify_files())

    def create_classes_clean(self, json_dictionary, lang):
        """Public entry point to creating classes from JSON schema.

        Args:
            json_dictionary - The JSON formatted dictionary.
            lang - The desired programming language for the JCONF output
        """
        del self.classes[:]
        self._parse_json_schema(json_dictionary, lang)
        return self.classes

    def _parse_json_schema(self, json_dictionary, lang):
        """Parse through the passed in dictionary that must be in the format
        defined by json-schema.org and create the class from it.

        Args:
            json_dictionary - The JSON formatted dictionary.
            lang - The desired programming language for the JCONF output
        """
        key_list = list(json_dictionary)
        if "type" in key_list and "title" in key_list and "properties" in key_list:
            if isinstance(json_dictionary["type"], str) and \
               isinstance(json_dictionary["title"], str) and \
               isinstance(json_dictionary["properties"], dict):

                class_maker = MakerFactory.get_maker(lang, json_dictionary["title"])
                class_members = json_dictionary["properties"]
                for member in class_members:
                    self._handle_clean_member(class_maker, member, class_members[member], lang)

                self.classes.extend(class_maker.stringify_files())


    def _handle_clean_member(self, class_maker, member, member_object, language):
        """Add the different class attributes to the class maker object.

        Args:
            class_maker - A class make object on which we will add the class attributes.
            member - The name of the current attribute
            member_object - json-schema defined property that contains information about
                            the particular attribute, most importantly, type!
            language - The target language for the created class
        """
        if "type" in member_object and isinstance(member_object["type"], str):
            if member_object["type"] == "string":
                class_maker.add_string(member, "")
            elif member_object["type"] == "integer" or member_object["type"] == "number":
                class_maker.add_number(member, 0.0)
            elif member_object["type"] == "boolean":
                class_maker.add_boolean(member, False)
            elif member_object["type"] == "object":
                class_maker.add_class(member)
                self._parse_json_schema(member_object, language)
            elif member_object["type"] == "array":
                if "items" in member_object and isinstance(member_object["items"], dict):
                    if "type" in member_object["items"] and\
                       isinstance(member_object["items"]["type"], str):
                        if member_object["items"]["type"] == "string":
                            class_maker.add_list(member, ClassMaker.Types.STRING)
                        if member_object["items"]["type"] == "integer" or\
                           member_object["items"]["type"] == "number":
                            class_maker.add_list(member, ClassMaker.Types.DOUBLE)
                        if member_object["items"]["type"] == "boolean":
                            class_maker.add_list(member, ClassMaker.Types.BOOLEAN)


def setup_cl_args():
    """Create the command line arguments for the tool.

    Returns:
        Returns the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="The program will parse a JSON \
                                                  configuration file and produce C++ output files")
    parser.add_argument("-d",
                        type=str,
                        metavar="class name",
                        dest="class_name",
                        help="If run in dirty mode, specify class name")
    parser.add_argument("-l",
                        type=str,
                        metavar="language",
                        dest="language",
                        default="cpp",
                        help="The desired output language")
    parser.add_argument("file",
                        type=str,
                        metavar="file",
                        help="Name of JSON file")
    return parser.parse_args()

if __name__ == '__main__':
    """If the JSON Class Utility is run as the main program then we just
    create the classes. Currently, we do not do anything with them, however.
    """

    jcutil = Jcu()

    # Set up arguments needed for running the program
    ARGS = setup_cl_args()

    if ARGS.file:
        # Actually open the file.
        with open(ARGS.file, 'r') as f:
            try:
                CLASS_LIST = []
                JSON_INFO = json.load(f)
                if ARGS.class_name:
                    CLASS_LIST = jcutil.create_classes_dirty(JSON_INFO,\
                                                             ARGS.class_name,\
                                                             ARGS.language)
                else:
                    CLASS_LIST = jcutil.create_classes_clean(JSON_INFO, ARGS.language)

                for class_tuple in CLASS_LIST:
                    print(class_tuple.file_name)
            except json.JSONDecodeError as error:
                print("Invalid JSON file at line " + str(error.lineno))
