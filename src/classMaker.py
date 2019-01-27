"""Credit to David Monts, circa 2017

The classMaker module.

This module provides the basic helper functions needed by
all of the different language-specific modules.
"""

from collections import namedtuple

Class_file = namedtuple('Class_file', ['file_name', 'file_contents'])

class ClassMaker(object):
    """Base class for all of the language-specific classes.
    """

    class Types():
        """Defines the different possible types that can be retrieved
        the JSON text.
        """
        CLASS = "dict"
        STRING = "str"
        DOUBLE = "float"
        ARRAY = "list"
        BOOLEAN = "bool"

    def __init__(self, name):
        """Initializes all of the class memebers to acceptable values.

        Args:
            name: The desired name for the class.
        """

        self.code_lines = []
        self.class_name = name
        self.string_found = False
        self.list_found = False
        self.string_list = []
        self.number_list = []
        self.list_list = []
        self.class_list = []
        self.boolean_list = []

    def add_string(self, string_name, init_string):
        """Add the name of a string to the class.

        Args:
            string_name: The name of a JSON key whose value is a string.
        """
        self.string_list.append((string_name, init_string))

    def add_number(self, number_name, init_number):
        """Add the name of a number to the class.

        Args:
            number_name: The name of a JSON key whose value is a number.
        """
        self.number_list.append((number_name, init_number))

    def add_list(self, list_name, list_type):
        """Add the name and type of a list to the class.

        Args:
            list_name: The name of a JSON key whose value is a list.
            list_type: The type of JSON list.
        """
        self.list_list.append((list_name, list_type))

    def add_class(self, class_name):
        """Add the name of another class to the class.

        Args:
            class_name: The name of a JSON key whose value is a class itself.
        """
        self.class_list.append(class_name)

    def add_boolean(self, boolean_name, init_boolean):
        """Add the name of boolean to the class.

        Args:
            boolean_name: The name of a JSON key whose value is a boolean.
        """
        self.boolean_list.append((boolean_name, init_boolean))

    def stringify_files(self):
        """Returns a tuple representing the different file names
        and the file contents
        """
        return []

    def _capitalize_first_letter(self, word):
        """Capitalizes the first letter of the word

        Args:
            word - Word in need of a capital first letter

        Returns:
            Returns the same word execpt with the first letter capitalized.
        """
        if len(word) > 0:
            first_letter = word[0]
            first_letter = first_letter.upper()
            return first_letter + word[1:]
        return ""
