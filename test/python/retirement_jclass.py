import json

class Retirement_jclass(object):

	def __init__(self):
		self.location = "New Orleans"
		self.money = True

	def classify(self, json_string):
		result_info = []
		parsed_json = json.loads(json_string)

		if(type(parsed_json["location"]) == str):
			self.location = parsed_json["location"]
		else:
			result_info.append("Incorrect type: location")

		if(type(parsed_json["money"]) == bool):
			self.money = parsed_json["money"]
		else:
			result_info.append("Incorrect type: money")

		return result_info

	def unclassify(self):
		myself = {}

		myself["location"] = self.location
		myself["money"] = self.money

		return json.dumps(myself, indent = 3)
