import json
from retirement_jclass import Retirement_jclass
from children_jclass import Children_jclass

class Family_jclass(object):

	def __init__(self):
		self.wife = "doe"
		self.husband = "john"
		self.retirement = Retirement_jclass()
		self.children = []
		self.hobbies = []
		self.house = True

	def classify(self, json_string):
		result_info = []
		parsed_json = json.loads(json_string)

		if(type(parsed_json["wife"]) == str):
			self.wife = parsed_json["wife"]
		else:
			result_info.append("Incorrect type: wife")

		if(type(parsed_json["husband"]) == str):
			self.husband = parsed_json["husband"]
		else:
			result_info.append("Incorrect type: husband")

		if(type(parsed_json["house"]) == bool):
			self.house = parsed_json["house"]
		else:
			result_info.append("Incorrect type: house")

		if(type(parsed_json["retirement"]) == dict):
			result_info.extend(self.retirement.classify(json.dumps(parsed_json["retirement"])))
		else:
			result_info.append("Incorrect type: retirement")

		self.children = []
		if(type(parsed_json["children"]) == list):
			for each in parsed_json["children"]:
				if(type(each) == dict):
					new_children = Children_jclass()
					result_info.extend(new_children.classify(json.dumps(each)))
					self.children.append(new_children)
				else:
					result_info.append("Incorrect type in list: children")
		else:
			result_info.append("Incorrect type: children")

		self.hobbies = []
		if(type(parsed_json["hobbies"]) == list):
			for each in parsed_json["hobbies"]:
				if(type(each) == str):
					self.hobbies.append(each)
				else:
					result_info.append("Incorrect type in list: hobbies")
		else:
			result_info.append("Incorrect type: hobbies")

		return result_info

	def unclassify(self):
		myself = {}

		myself["wife"] = self.wife
		myself["husband"] = self.husband
		myself["house"] = self.house
		myself["retirement"] = json.loads(self.retirement.unclassify())
		myself["children"] = []
		for each in self.children:
			myself["children"].append(json.loads(each.unclassify()))
		myself["hobbies"] = self.hobbies

		return json.dumps(myself, indent = 3)
