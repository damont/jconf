"""Credit to David Monts, circa 2017

The csharpClassMaker module.

This module provides the functionality needed to create files
for C# classes.
"""

from classMaker import *

class CsharpClassMaker(ClassMaker):
	"""Creates C# class files.
	"""
	
	CSHARP_EXT = "Jclass"
	
	def __init__(self, name):
		"""The constructor for the class simply calls the constructor for the base class
		as the class does not need any extra member variables
		"""
		ClassMaker.__init__(self, name)
		self.class_name = self.class_name + self.CSHARP_EXT
		
	def _get_imports(self):
		"""Returns a list of imports for the class.
		
		Returns:
			Returns the needed using statements for the class
		"""
		import_lines = []
		
		if self.list_list:
			import_lines.append("using System.Collections.Generic;")
		import_lines.append("\n")	
		return import_lines
			
	def _get_class_start(self):
		"""Provides the class header for C# classes
		
		Returns:
			The class header for C# classes
		"""
		class_header_list = []
		class_header_list.append("class " + self._capitalize_first_letter(self.class_name))
		class_header_list.append("{")
		class_header_list.append("\n")
		
		for string in self.string_list:
			class_header_list.append("\tpublic string " + string[0] + ";")
		for number in self.number_list:
			class_header_list.append("\tpublic double " + number[0] + ";")
		for class_name in self.class_list:
			class_header_list.append("\tpublic " + self._capitalize_first_letter(class_name + self.CSHARP_EXT) + " " + class_name + ";")
		for list in self.list_list:
			if list[1] == self.Types.CLASS:
				class_header_list.append("\tpublic IList<" + self._capitalize_first_letter(list[0] + self.CSHARP_EXT) + "> " + list[0] + ";")
			elif list[1] == self.Types.STRING:
				class_header_list.append("\tpublic IList<string> " + list[0] + ";")
			elif list[1] == self.Types.DOUBLE:
				class_header_list.append("\tpublic IList<double> " + list[0] + ";")
			elif list[1] == self.Types.BOOLEAN:
				class_header_list.append("\tpublic IList<bool> " + list[0] + ";")
		for boolean in self.boolean_list:
			class_header_list.append("\tpublic bool " + boolean[0] + ";")
		
		class_header_list.append("\n")
		return class_header_list
		
	def _get_init_func(self):
		"""Provides the constructor for the C# class
		
		Returns:
			A list of the lines for the constructor
		"""
		constructor_list = []
		constructor_list.append("\tpublic " + self._capitalize_first_letter(self.class_name) + "()")
		constructor_list.append("\t{")
		for string in self.string_list:
			constructor_list.append("\t\t" + string[0] + " = \"" + string[1] + "\";")
		for number in self.number_list:
			constructor_list.append("\t\t" + number[0] + " = " + str(number[1]) + ";")
		for class_name in self.class_list:
			constructor_list.append("\t\t" + class_name + " = new " + self._capitalize_first_letter(class_name + self.CSHARP_EXT) + "();")
		for list in self.list_list:
			if list[1] == self.Types.CLASS:
				constructor_list.append("\t\t" + list[0] + "= new List<" + self._capitalize_first_letter(list[0] + self.CSHARP_EXT) + ">();")
			elif list[1] == self.Types.STRING:
				constructor_list.append("\t\t" + list[0] + "IList<string>();")
			elif list[1] == self.Types.DOUBLE:
				constructor_list.append("\t\t" + list[0] + "IList<double>();")
			elif list[1] == self.Types.BOOLEAN:
				constructor_list.append("\t\t" + list[0] + "IList<bool>();")
		for boolean in self.boolean_list:
			constructor_list.append("\t\t" + boolean[0] + " = " + (str(boolean[1])).lower() + ";")
		constructor_list.append("\t}")
		constructor_list.append("\n")
		return constructor_list
		
	def _get_class_end(self):
		"""Place holder. This function must be overridden
		by children classes.
		"""
		end_list = []
		end_list.append("}")
		return end_list
		
	def stringify_files(self):
		"""Create C# class file

		Returns an array containing one tuple which includes the file name and the file contents
		"""
		csharp_file = []
		csharp_file.extend(self._get_imports())
		csharp_file.extend(self._get_class_start())
		csharp_file.extend(self._get_init_func())
		csharp_file.extend(self._get_classify_func())
		csharp_file.extend(self._get_unclassify_func())
		csharp_file.extend(self._get_class_end())

		csharp_string = ""
		for line in csharp_file:
			csharp_string += line + "\n"
		
		csharp_tuple = Class_file(self.class_name + ".cs", csharp_string)

		csharp_array = [csharp_tuple]

		return csharp_array
	