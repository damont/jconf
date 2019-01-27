import json

class Children_jclass(object):

	def __init__(self):
		self.name = "kiddo"
		self.age = 1.0

	def classify(self, json_string):
		result_info = []
		parsed_json = json.loads(json_string)

		if(type(parsed_json["name"]) == str):
			self.name = parsed_json["name"]
		else:
			result_info.append("Incorrect type: name")

		if((type(parsed_json["age"]) == int) or (type(parsed_json["age"]) == float)):
			self.age = parsed_json["age"]
		else:
			result_info.append("Incorrect type: age")

		return result_info

	def unclassify(self):
		myself = {}

		myself["name"] = self.name
		myself["age"] = self.age

		return json.dumps(myself, indent = 3)
