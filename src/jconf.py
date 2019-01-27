#!/user/bin/python
"""Credit to David Monts, circa 2017

The JSON Configuration tool!!!

For more information, python jconf.py -h 
"""

import argparse
import json
from pprint import pprint
from classMaker import *
from makerFactory import MakerFactory
import tkinter as tk

def setup_cl_args():
	"""Create the command line arguments for the tool.
	
	Returns:
		Returns the parsed arguments.
	"""
	parser = argparse.ArgumentParser(description="The program will parse a JSON configuration file and produce C++ output files")
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
	parser.add_argument("-f",
									 type=str,
									 metavar="file", 
									 dest="file",
									 help="Name of JSON file")
	return parser.parse_args()

def create_classes_dirty(ji, ji_name, lang):
	"""Parse through the passed in dictionary and create the class from it.
	
	Args:
		ji - The JSON formatted dictionary.
		ji_name - The name that will be the class name
		lang - The desired programming language for the JCONF output
	"""
	cm = MakerFactory.get_maker(lang, ji_name)
	if cm:
		for key in ji:
			if(type(ji[key]) == dict):
				cm.add_class(key)
				create_classes_dirty(ji[key], key, lang)
			if(type(ji[key]) == str):
				cm.add_string(key, ji[key])
			if(type(ji[key]) == float):
				cm.add_number(key, ji[key])
			if(type(ji[key]) == int):
				cm.add_number(key, float(ji[key]))
			if(type(ji[key]) == list):
				if ji[key]:
					first = ji[key][0]
					if(type(first) == dict):
						cm.add_list(key, ClassMaker.Types.CLASS)
						create_classes_dirty(ji[key][0], key, lang)
					if(type(first) == str):
						cm.add_list(key, ClassMaker.Types.STRING)
					if(type(first) == float) or (type(first) == int):
						cm.add_list(key, ClassMaker.Types.DOUBLE)
					if(type(first) == list):
						cm.add_list(key, ClassMaker.Types.ARRAY)
					if(type(first) == bool):
						cm.add_list(key, ClassMaker.Types.BOOLEAN)
			if(type(ji[key]) == bool):
				cm.add_boolean(key, ji[key])
		cm.make_files()
		
def create_classes_clean(ji, lang):
	"""Parse through the passed in dictionary that must be in the format
	defined by json-schema.org and create the class from it.
	
	Args:
		ji - The JSON formatted dictionary.
		lang - The desired programming language for the JCONF output
	"""
	key_list = list(ji)
	if "type" in key_list and "title" in key_list and "properties" in key_list:
		if type(ji["type"]) == str and type(ji["title"]) == str and type(ji["properties"]) == dict:
			#We are good to go. Keep moving.
			cm = MakerFactory.get_maker(lang, ji["title"])
			class_members = ji["properties"]
			for member in class_members:
				handle_clean_member(cm, member, class_members[member], lang)
				
			return cm.stringify_files()

			
def handle_clean_member(class_maker, member, member_object, language):
	if "type" in member_object and type(member_object["type"]) == str:
		if member_object["type"] == "string":
			class_maker.add_string(member, "")
		elif member_object["type"] == "integer" or member_object["type"] == "number":
			class_maker.add_number(member, 0.0)
		elif member_object["type"] == "boolean":
			class_maker.add_boolean(member, False)
		elif member_object["type"] == "object":
			class_maker.add_class(member)
			create_classes_clean(member_object, language)
		elif member_object["type"] == "array":
			if "items" in member_object and type(member_object["items"]) == dict:
				if "type" in member_object["items"] and type(member_object["items"]["type"]) == str:
					if member_object["items"]["type"] == "string":
						class_maker.add_list(member, ClassMaker.Types.STRING)
					if member_object["items"]["type"] == "integer" or member_object["items"]["type"] == "number":
						class_maker.add_list(member, ClassMaker.Types.DOUBLE)
					if member_object["items"]["type"] == "boolean":
						class_maker.add_list(member, ClassMaker.Types.BOOLEAN)
				
class Application(tk.Frame):

	def __init__(self, master):
		tk.Frame.__init__(self, master)

		self.input_text = tk.Text(self, wrap="word", height=50)
		self.input_text.grid(row=0, column=0)
		
		self.output_text = tk.Text(self, wrap="word", height=50)
		self.output_text.grid(row=0, column=1)
		
		self.button_holder = tk.Frame(self)
		self.button_holder.grid(row=1, column=0, sticky="W")

		self.create_clean_button = tk.Button(self.button_holder, 
																text="Create Clean",
																padx=10,
																pady=5,
																command=self._generate_class)
		self.create_clean_button.grid(row=0, column=0, padx=10, pady=5)

		self.create_dirty_button = tk.Button(self.button_holder, 
																text="Create Dirty",
																padx=10,
																pady=5,
																command=self._generate_class)
		self.create_dirty_button.grid(row=0, column=1, padx=10, pady=5)
		
	def _generate_class(self):
		try:
			json_info = json.loads(self.input_text.get(1.0, tk.END))
			file_array = []
			file_array.extend(create_classes_clean(json_info, "csharp"))
			if file_array:
				self.output_text.delete(1.0, tk.END)
				self.output_text.insert(1.0, file_array[0].file_contents)
				self.output_text.insert(tk.END, "Got here atleast")
			else:
				self.output_text.insert(tk.END, "Got here with nothing")
		except json.JSONDecodeError as e:
			self.output_text.delete(1.0, tk.END)
			self.output_text.insert(1.0, "Invalid JSON file at line " + str(e.lineno))
	

if __name__ == '__main__':	
	# Set up arguments needed for running the program
	args = setup_cl_args()

	if args.file:		
		# Actually open the file.
		with open(args.file, 'r') as f:
			try:
				json_info = json.load(f)
				if args.class_name:
					create_classes_dirty(json_info, args.class_name, args.language)
				else:
					create_classes_clean(json_info, args.language)
			except json.JSONDecodeError as e:
				print("Invalid JSON file at line " + str(e.lineno))
	else:
		root = tk.Tk()
		app = Application(root).pack(side="top", fill="both", expand=True)
		root.mainloop()