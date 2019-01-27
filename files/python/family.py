import json
from children_jconf import Children_jconf

class Family(object):

	def __init__(self):
		self.husband = ""
		self.wife = ""
		self.children = []
		self.house = True
		self.hobbies = []

	def parse_string(self, json_string):
		result_info = []
		parsed_json = json.loads(json_string)
		
		if(type(parsed_json["husband"]) == str):
			self.husband = parsed_json["husband"]
		else:
			result_info.append("Incorrect type: husband")
		
		if((type(parsed_json["wife"]) == str)):
			self.wife = parsed_json["wife"]
		else:
			result_info.append("Incorrect type: wife")
		
		if((type(parsed_json["children"]) == list)):
			if parsed_json["children"][0]:
				for each in parsed_json["children"]:
					if(type(each) == dict):
						new_children = Children_jconf()
						result_info.extend(new_children.parse_dict(each))
						self.children.append(new_children)
					else:
						result.info.append("Incorrect list type: children")
		else:
			result_info.append("Incorrect type: children")
			
		if((type(parsed_json["house"]) == bool)):
			self.house = parsed_json["house"]
		else:
			result_info.append("Incorrect type: house")
		
		if((type(parsed_json["hobbies"]) == list)):
			self.house = parsed_json["hobbies"]
		else:
			result_info.append("Incorrect type: hobbies")
			
		if((type(parsed_json["retirement"]) == dict):
			result_info.extend(self.retirement.parse(json.dumps(parse_json["retirement"])))
		else:
			result_info.append("Incorrect type: retirement")
		
		
		return result_info