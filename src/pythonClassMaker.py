"""Credit to David Monts, circa 2017

The pythonClassMaker module.

This module inherits from the base class maker and uses the extracted
information in order to create a Python class for extracting JSON, verifying JSON,
and recreating JSON.
"""

from classMaker import *

class PythonClassMaker(ClassMaker):
	"""The Python class maker.
	"""
	
	PYTHON_EXT = "_jclass"
	
	def __init__(self, name):
		"""The constructor for the class simply calls the constructor for the base class
		as the class does not need any extra member variables
		"""
		ClassMaker.__init__(self, name)
		self.class_name = self.class_name + self.PYTHON_EXT
		
	def _get_imports(self):
		"""Adds all of the lines needed for importing information
		
		Returns: 
			The list of imports.
		"""
		import_list = []
		import_list.append("import json")
		for class_name in self.class_list:
			class_name = class_name + self.PYTHON_EXT
			import_list.append("from " + class_name + " import " + self._capitalize_first_letter(class_name))
		for list_tuple in self.list_list:
			if list_tuple[1] == self.Types.CLASS:
				class_name = list_tuple[0]
				class_name = class_name + self.PYTHON_EXT
				import_list.append("from " + class_name + " import " + self._capitalize_first_letter(class_name))
		import_list.append("\n")
		return import_list
			
	def _get_class_start(self):
		"""Adds the class name
		
		Returns:
			A list containing the class name
		"""
		class_name_caps = self._capitalize_first_letter(self.class_name)
		class_name_list = []
		class_name_list.append("class " + class_name_caps + "(object):")
		class_name_list.append("\n")
		return class_name_list
		
	def _get_init_func(self):
		"""Creates everything needed for the constructor of the class
		
		Returns:
			A list containing all of the lines of the constructor
		"""	
		init_list = []
		init_list.append("\tdef __init__(self):")
		for string in self.string_list:
			init_list.append("\t\tself." + string[0] + " = \"" + string[1] + "\"")
		for number in self.number_list:
			init_list.append("\t\tself." + number[0] + " = " + str(float(number[1])))
		for class_name in self.class_list:
			init_list.append("\t\tself." + class_name + " = " + self._capitalize_first_letter(class_name + self.PYTHON_EXT) + "()")
		for list in self.list_list:
			init_list.append("\t\tself." + list[0] + " = []")
		for boolean in self.boolean_list:
			init_list.append("\t\tself." + boolean[0] + " = "+ str(boolean[1]))
		init_list.append("\n")
		return init_list
		
		
	def _get_classify_func(self):
		"""Creates everything needed to ensure the JSON is correct and 
		extract that JSON into the appropriate member variable
		
		Returns:
			A list containing the lines for the function which parses and extracts the JSON
		"""
		parse_func_list = []
		parse_func_list.append("\tdef classify(self, json_string):")
		parse_func_list.append("\t\tresult_info = []")
		parse_func_list.append("\t\tparsed_json = json.loads(json_string)")
		
		for string in self.string_list:
			parse_func_list.append("\n")
			parse_func_list.append("\t\tif(type(parsed_json[\"" + string[0] + "\"]) == str):")
			parse_func_list.append("\t\t\tself." + string[0] + " = parsed_json[\"" + string[0] + "\"]")
			parse_func_list.append("\t\telse:")
			parse_func_list.append("\t\t\tresult_info.append(\"Incorrect type: " + string[0] + "\")")
			
		for number in self.number_list:
			parse_func_list.append("\n")
			parse_func_list.append("\t\tif((type(parsed_json[\"" + number[0] + "\"]) == int) or (type(parsed_json[\"" + number[0] + "\"]) == float)):")
			parse_func_list.append("\t\t\tself." + number[0] + " = parsed_json[\"" + number[0] + "\"]")
			parse_func_list.append("\t\telse:")
			parse_func_list.append("\t\t\tresult_info.append(\"Incorrect type: " + number[0] + "\")")
			
		for boolean in self.boolean_list:
			parse_func_list.append("\n")
			parse_func_list.append("\t\tif(type(parsed_json[\"" + boolean[0] + "\"]) == bool):")
			parse_func_list.append("\t\t\tself." + boolean[0] + " = parsed_json[\"" + boolean[0] + "\"]")
			parse_func_list.append("\t\telse:")
			parse_func_list.append("\t\t\tresult_info.append(\"Incorrect type: " + boolean[0] + "\")")
		
		for class_name in self.class_list:
			parse_func_list.append("\n")
			parse_func_list.append("\t\tif(type(parsed_json[\"" + class_name + "\"]) == dict):")
			parse_func_list.append("\t\t\tresult_info.extend(self." + class_name + ".classify(json.dumps(parsed_json[\"" + class_name + "\"])))")
			parse_func_list.append("\t\telse:")
			parse_func_list.append("\t\t\tresult_info.append(\"Incorrect type: " + class_name + "\")")

		for list_tuple in self.list_list:
			parse_func_list.append("\n")
			parse_func_list.append("\t\tself." + list_tuple[0] + " = []")
			parse_func_list.append("\t\tif(type(parsed_json[\"" + list_tuple[0] + "\"]) == list):")
			parse_func_list.append("\t\t\tfor each in parsed_json[\"" + list_tuple[0] + "\"]:")
			parse_func_list.append("\t\t\t\tif(type(each) == " + list_tuple[1] + "):")
			if list_tuple[1] == self.Types.CLASS:
				parse_func_list.append("\t\t\t\t\tnew_" + list_tuple[0] + " = " + self._capitalize_first_letter(list_tuple[0] + self.PYTHON_EXT) + "()")
				parse_func_list.append("\t\t\t\t\tresult_info.extend(new_" + list_tuple[0] + ".classify(json.dumps(each)))")
				parse_func_list.append("\t\t\t\t\tself."+ list_tuple[0] + ".append(new_"+ list_tuple[0] + ")")
			else:				
				parse_func_list.append("\t\t\t\t\tself." + list_tuple[0] + ".append(each)")
			parse_func_list.append("\t\t\t\telse:")
			parse_func_list.append("\t\t\t\t\tresult_info.append(\"Incorrect type in list: " + list_tuple[0] + "\")")
			parse_func_list.append("\t\telse:")
			parse_func_list.append("\t\t\tresult_info.append(\"Incorrect type: " + list_tuple[0] + "\")")
		
		parse_func_list.append("\n")
		parse_func_list.append("\t\treturn result_info")
		parse_func_list.append("\n")
			
		return parse_func_list
		
	def _get_unclassify_func(self):
		"""Creates everything needed for a function that returns the class data
		in JSON format as a string.
		
		Returns:
			A list containing the lines for the function which reproduces the JSON
		"""
		unparse_func_list = []
		unparse_func_list.append("\tdef unclassify(self):")
		unparse_func_list.append("\t\tmyself = {}")
		unparse_func_list.append("\n")
		
		for string in self.string_list:
			unparse_func_list.append("\t\tmyself[\"" + string[0] + "\"] = self." + string[0])
			
		for number in self.number_list:
			unparse_func_list.append("\t\tmyself[\"" + number[0] + "\"] = self." + number[0])
			
		for boolean in self.boolean_list:
			unparse_func_list.append("\t\tmyself[\"" + boolean[0] + "\"] = self." + boolean[0])
		
		for class_name in self.class_list:
			unparse_func_list.append("\t\tmyself[\"" + class_name + "\"] = json.loads(self." + class_name + ".unclassify())")
			
		for list_tuple in self.list_list:
			if list_tuple[1] == self.Types.CLASS:
				unparse_func_list.append("\t\tmyself[\"" + list_tuple[0] + "\"] = []")
				unparse_func_list.append("\t\tfor each in self." + list_tuple[0] + ":")
				unparse_func_list.append("\t\t\tmyself[\"" + list_tuple[0] + "\"].append(json.loads(each.unclassify()))")
			else:				
				unparse_func_list.append("\t\tmyself[\"" + list_tuple[0] + "\"] = self." + list_tuple[0])
		
		unparse_func_list.append("\n")
		unparse_func_list.append("\t\treturn json.dumps(myself, indent = 3)")
			
		return unparse_func_list
		
	def stringify_files(self):
		"""Create Python class file

		Returns an array containing one tuple which includes the file name and the file contents
		"""
		py_file = []
		py_file.extend(self._get_imports())
		py_file.extend(self._get_class_start())
		py_file.extend(self._get_init_func())
		py_file.extend(self._get_classify_func())
		py_file.extend(self._get_unclassify_func())

		py_string = ""
		for line in py_file:
			py_string += line + "\n"
		
		py_tuple = Class_file(self.class_name + ".py", py_string)

		py_array = [py_tuple]

		return py_array