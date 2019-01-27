import json

class Children_jconf(object):

	def __init__(self):
		self.name = ""
		self.age = 0

	def parse_string(self, json_string):
		result_info = []
		parsed_json = json.loads(json_string)
		
		if(type(parsed_json["name"]) == str):
			self.name = parsed_json["name"]
		else:
			result_info.append("Incorrect type: name")
		
		if((type(parsed_json["age"]) == float) or
		   (type(parsed_json["age"]) == int)):
			self.age = parsed_json["age"]
		else:
			result_info.append("Incorrect type: age")
		
		return result_info
		
	def parse_dict(self, json_dict):
		result_info = []
		if(type(json_dict["name"]) == str):
			self.name = json_dict["name"]
		else:
			result_info.append("Incorrect type: name")
		
		if((type(json_dict["age"]) == float) or
		   (type(json_dict["age"]) == int)):
			self.age = json_dict["age"]
		else:
			result_info.append("Incorrect type: age")
		
		return result_info