"""The derived class responsible for developing C++ files
"""

from classMaker import *

class CppClassMaker(ClassMaker):
	"""Creates C++ class files.
	"""
	
	CPP_EXT = "_Jclass"
	
	def __init__(self, name):
		"""The constructor for the class simply calls the constructor for the base class
		as the class does not need any extra member variables
		"""
		ClassMaker.__init__(self, name)
		self.class_name = self.class_name + self.CPP_EXT
		
	def _get_imports(self):
		"""Returns a list of imports for the class.
		
		Returns:
			Returns the needed include statements for the class
		"""
		import_lines = []
		
		if self.list_list:
			import_lines.append("include <deque>")
		for lis in self.list_list:
			if(lis[1] == ClassMaker.Types.CLASS):
				import_lines.append("include \"" + self._capitalize_first_letter(lis[0] + self.CPP_EXT) + ".h\"")
		if self.string_list:
			import_lines.append("include <string>")
		for clss in self.class_list:
			import_lines.append("include \"" + self._capitalize_first_letter(clss + self.CPP_EXT) + ".h\"")
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
		class_header_list.append("public:")
		
		for string in self.string_list:
			class_header_list.append("\tstring " + string[0] + ";")
		for number in self.number_list:
			class_header_list.append("\tdouble " + number[0] + ";")
		for class_name in self.class_list:
			class_header_list.append("\t" + self._capitalize_first_letter(class_name + self.CPP_EXT) + " " + class_name + ";")
		for list in self.list_list:
			if list[1] == self.Types.CLASS:
				class_header_list.append("\tdeque<" + self._capitalize_first_letter(list[0] + self.CPP_EXT) + "> " + list[0] + ";")
			elif list[1] == self.Types.STRING:
				class_header_list.append("\tdeque<string> " + list[0] + ";")
			elif list[1] == self.Types.DOUBLE:
				class_header_list.append("\tdeque<double> " + list[0] + ";")
			elif list[1] == self.Types.BOOLEAN:
				class_header_list.append("\tdeque<bool> " + list[0] + ";")
		for boolean in self.boolean_list:
			class_header_list.append("\tbool " + boolean[0] + ";")
		
		class_header_list.append("\n")
		return class_header_list
		
	def _get_class_end(self):
		"""Place holder. This function must be overridden
		by children classes.
		"""
		end_list = []
		end_list.append("}")
		return end_list
		
	def stringify_files(self):
		"""Create the .hpp and .cpp files.

		Returns an array containing two tuples, one for the .hpp file and one for the .cpp file
		"""
		cpp_file = []
		cpp_file.extend(self._get_imports())
		cpp_file.extend(self._get_class_end())
		cpp_file.extend(self._get_class_start())

		cpp_string = ""
		for line in cpp_file:
			cpp_string += line + "\n"
		
		cpp_tuple = Class_file(self.class_name + ".cpp", cpp_string)
		print(cpp_tuple.file_name)

		cpp_array = [cpp_tuple]
		print(cpp_array[0].file_name)
		print(cpp_array[0].file_contents)

		return cpp_array