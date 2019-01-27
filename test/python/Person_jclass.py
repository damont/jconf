import json

class Person_jclass(object):

	def __init__(self):
		self.lastName = ""
		self.firstName = ""
		self.age = 0.0

	def classify(self, json_string):
		result_info = []
		parsed_json = json.loads(json_string)

		if(type(parsed_json["lastName"]) == str):
			self.lastName = parsed_json["lastName"]
		else:
			result_info.append("Incorrect type: lastName")

		if(type(parsed_json["firstName"]) == str):
			self.firstName = parsed_json["firstName"]
		else:
			result_info.append("Incorrect type: firstName")

		if((type(parsed_json["age"]) == int) or (type(parsed_json["age"]) == float)):
			self.age = parsed_json["age"]
		else:
			result_info.append("Incorrect type: age")

		return result_info

	def unclassify(self):
		myself = {}

		myself["lastName"] = self.lastName
		myself["firstName"] = self.firstName
		myself["age"] = self.age

		return json.dumps(myself, indent = 3)
